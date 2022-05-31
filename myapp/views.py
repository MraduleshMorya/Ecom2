import email
from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

from itertools import product
from django import http
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from requests import request
from .models import users,orders,items,image_db
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate



import json
global is_admin



#request.session["username"] = None
def index(request):
    return redirect('loginpage')
    # return HttpResponse("empty path")

def loginpage(request):
    # print(request.session)
    # print(request.session["username"])
    if "username" in request.session:
        del request.session['username']
        
    get_items = items.objects.all().values()
    context = {"items": get_items}
    print(context)
    return render(request,"login.html",context)


def logout(request): 
    print("request-- ", request) 
    global is_admin
    is_admin = False
    if "username" in request.session:
        del request.session['username']
    #logout(request)
    return redirect('loginpage')
    

# Create your views here.
def login(request):
    input_username = request.POST['input_username']
    input_password = request.POST['input_password']
    request.session["username"] = input_username
   
    user = authenticate(request, username=input_username, password=input_password)
    check_username = authenticate(request, username=input_username)
    
    print("username", check_username)
    
    if user is not None:
        #login(request,user)
        request.session["username"] = input_username
        request.session.modified = True
        return redirect('loggedin')
    elif check_username is None :
        passed_massage = {"massage": " invalid username "}
        return render(request,"login.html",passed_massage)
    else:
        passed_massage = {"massage": " wrong password"}
        return render(request,"login.html",passed_massage)
    
         

def signup(request):
    
        input_username = request.POST['signusername']
        input_first_name = request.POST['firstname']
        input_last_name = request.POST['lastname']
        input_email = request.POST['email']
        input_password = request.POST['password']
        input_address = request.POST['address']
        
        filtered_username = users.objects.filter(username= input_username)
        filtered_email = users.objects.filter(email= input_email)
        
        
        if filtered_username:
            passed_massage= {"massage": "username already exist "}
            return render(request,"login.html",passed_massage)
            # return redirect(request.META['HTTP_REFERER'],passed_massage)
        elif filtered_email:
            passed_massage= {"massage": "email already exist "}
            return render(request,"login.html",passed_massage)
        else:
            input_data = users(username = input_username, first_name = input_first_name, last_name = input_last_name,email = input_email, password = input_password, address = input_address)
            input_data.save()  
            user = User.objects.create_user(input_username, input_email, input_password)
            user.first_name = input_first_name
            user.last_name = input_last_name
            user.save()
            
            get_username = User.objects.get(username=input_username)
            
            print("get username -", get_username)
            
            passed_massage = {"massage": "sign up success , please login "}      
            return render(request,"login.html",passed_massage)
            # return redirect(request.META['HTTP_REFERER'],passed_massage)
    
    
def loggedin(request):
    
    print(request.session)
    print(request.session["username"])
    
    #place_order = items.objects.filter(name=product_name)
    if "username"  not in request.session:
        return redirect ("loginpage")
    
    get_user_data = users.objects.filter(username = request.session["username"]).values()
    get_items = items.objects.all()
    
    
    get_ordered = orders.objects.filter(username = request.session["username"]).exclude(status='cart').values()
    
    
    user_data ={"data": get_user_data}
    item_data = {"item": get_items}
    orders1 ={"order": get_ordered}
    
    
    context = {"user_data": user_data,"item_data": item_data,"orders1": orders1}
                
    return render(request,"product&profile.html",context)
    
            

def user_profile(request):
    username = request.session["username"]
    user_detail = users.objects.filter(username = username)
    
    context = {"user_detail": user_detail}
    return render(request, "user_profile.html", context)

            
def placeorder(request, id ):
    print("place order")
    if "username" not in request.session:
        return redirect ("loginpage")
    
    print(request.session["username"])
    orders.objects.filter(oreder_id = id ).update(orderid=3, status ="unverified")
    return redirect('user_cart_details')
    #return render(request,"login.html")



def order_manage(request):
    if is_admin == True:
        get_user_data = users.objects.all().values()
        get_ordered = orders.objects.exclude(status = "cart").values()
        
        user_data ={"data": get_user_data}
        orders1 ={"order": get_ordered}
        #context = {"user_data": user_data,"orders1": orders1}
        
        pending_orders2 = orders.objects.filter(status = 'confirmation pending').values()
        confirm_orders2 = orders.objects.filter(status = 'confirmed').values()
        declined_orders2 = orders.objects.filter(status = 'declined').values()
        dispatched_orders2 = orders.objects.filter(status = 'dispatched').values()
        delivered_orders2 = orders.objects.filter(status = 'delivered').values()
        
        print(dispatched_orders2)

        pending_orders = {"orders": pending_orders2}
        confirm_orders = {"orders": confirm_orders2}
        declined_orders ={"orders": declined_orders2}
        dispatched_orders ={"orders": dispatched_orders2}
        delivered_orders = {"orders": delivered_orders2}



        context = {"user_data": user_data,"orders1": orders1,"uncon_orders": pending_orders, "con_orders": confirm_orders , "declined_orders": declined_orders, "delivered_orders":delivered_orders, "dispatched_orders": dispatched_orders}

        return render(request, "admin.html", context)
    else :
        return redirect(request.META['HTTP_REFERER'])
    
    
    
def add_to_cart(request, item_name, item_price, user_address):
    print("add to cart")
    
    if "username" not in request.session:
        return redirect ("loginpage")
    
    print("add to cart running ")
    orders_obj = orders(username = request.session["username"], orderid = 0, item = item_name, price = item_price, status="cart", address=user_address)
    orders_obj.save()
    return redirect(request.META["HTTP_REFERER"])
    #return redirect("user_cart_details")



def delete_from_cart(request , item_order_id):
    if "username" not in request.session:
        return redirect ("loginpage")
    
    orders_db_obj = orders.objects.filter(oreder_id = item_order_id).delete()
    #orders_db_obj.delete()
    #orders_db_obj.save()
    return redirect (request.META['HTTP_REFERER'])



def user_cart_details(request):
    if "username" not in request.session:
        return redirect ("loginpage")
    
    print("user cart running ")
    orders_in_cart = orders.objects.filter(status = "cart",username = request.session["username"]).values()
    get_user_data = users.objects.filter(username = request.session["username"]).values()
    orders_in_cart_deatils ={"orders": orders_in_cart}
    user_data ={"data": get_user_data}
    
    context = {"cart_datails":orders_in_cart_deatils, "user_data": user_data}
    
    return render(request, "user_cart.html", context)


def user_placed_orders(request):
    if "username" not in request.session:
        return redirect ("loginpage")
    
    get_user_data = users.objects.filter(username = request.session["username"]).values()
    get_ordered = orders.objects.filter(username= request.session["username"]).exclude(status = "cart").values()
    
    user_data ={"data": get_user_data}
    orders1 ={"order": get_ordered}
    #context = {"user_data": user_data,"orders1": orders1}
    
    pending_orders2 = orders.objects.filter(status = 'confirmation pending').values()
    confirm_orders2 = orders.objects.filter(status = 'confirmed').values()
    declined_orders2 = orders.objects.filter(status = 'declined').values()
    dispatched_orders2 = orders.objects.filter(status = 'dispatched').values()
    delivered_orders2 = orders.objects.filter(status = 'delivered').values()

    pending_orders = {"orders": pending_orders2}
    confirm_orders = {"orders": confirm_orders2}
    declined_orders ={"orders": declined_orders2}
    dispatched_orders ={"orders": dispatched_orders2}
    delivered_orders = {"orders": delivered_orders2}



    context = {"user_data": user_data,"orders1": orders1,"uncon_orders": pending_orders, "con_orders": confirm_orders , "declined_orders": declined_orders, "delivered_orders":delivered_orders, "dispatched_orders": dispatched_orders}
    
                
    return render(request,"user_orders.html",context)   

def orderall(request, passed_username):
    orders.objects.filter(username= passed_username, status='cart').update(status="unverified")
    return redirect (request.META["HTTP_REFERER"])
 
def cancel_order(request, id):
    if "username" not in request.session:
        return redirect ("loginpage")
    
    cancelorder = orders.objects.filter(oreder_id = id)
    cancelorder.delete()
    cancelorder.save()
    return redirect(request.META["HTTP_REFERER"])

##
## admin functions 
##


def admin_login(request):
    get_username = request.POST["input_username"]
    get_password = request.POST["input_password"]
    
    global is_admin 
    is_admin = True 
    

    if get_username == 'admin' and get_password == 'admin':
        return redirect("order_manage")
    elif get_username == 'orderpro' and get_password == 'orderpro':
        # get_unverified_orders = orders.objects.filter(status= 'unverified')
        # context = {"orders":get_unverified_orders  }
        # return render(request,"order_processor.html", context)
        return redirect("op_login")


    else :
        return redirect(request.META['HTTP_REFERER'])
    
    
def order_processor_login(request):
    get_username = request.POST["input_username"]
    get_password = request.POST["input_password"]
    if get_username == 'orderpro' and get_password == 'orderpro':
        # get_unverified_orders = orders.objects.filter(status= 'unverified')
        # context = {"orders":get_unverified_orders  }
        # return render(request,"order_processor.html", context)
        return redirect("op_login")
    
    
def op_login(request):
    get_unverified_orders = orders.objects.filter(status= 'unverified')
    context = {"orders":get_unverified_orders  }
    return render(request,"order_processor.html", context)
    
    
    
def manage_items(request):
    global is_admin
    if not is_admin:
        return redirect ("loginpage")
    
    get_items = items.objects.all()
    context = {"items": get_items}
    
    return render(request ,"crud_items_page.html", context)


    
def add_item(request,):
    global is_admin
    if not is_admin:
        return redirect ("loginpage")
    
    input_item_name = request.POST["item_name"]
    input_item_price = request.POST["item_price"]

    database_obj = items(name = input_item_name, price = input_item_price)
    database_obj.save()

    return redirect(request.META["HTTP_REFERER"])



def delete_item(request , item_name):
    global is_admin
    if not is_admin:
        return redirect ("loginpage")
    
    database_obj = items.objects.filter(name = item_name)
    database_obj.delete()
    
    return redirect(request.META["HTTP_REFERER"])



def confirm_order(request, username ,item , id ):
    if "username" not in request.session:
        return redirect ("loginpage")
    
    print(" confirm order called ")
    database_obj = orders.objects.get(oreder_id = id)
    print(database_obj.status)
    database_obj.status = 'confirmed'
    database_obj.save()
    return redirect (request.META['HTTP_REFERER'])



def decline_order(request, id):
    if "username" not in request.session:
        return redirect ("loginpage")
    
    print(" decline order called ")
    database_obj = orders.objects.get(oreder_id = id)
    print(database_obj.status)
    database_obj.status = 'declined'
    database_obj.save()
    return redirect (request.META['HTTP_REFERER'])


def change_status(request, id, new_status):
    
    print("change status called ")
    database_obj = orders.objects.get(oreder_id = id)

    database_obj.status = new_status
    database_obj.save()
    return redirect (request.META['HTTP_REFERER'])


def images(request):
    images = image_db.objects.all()
    print(images)
    context = {"images": images}
    return render(request,"images.html", context)


def practice_raw(request):
    for p in users.objects.raw('SELECT username,first_name FROM myapp_users'):
        print(p.first_name)
        
    name_map = {'first_name': 'first_name', 'last_name': 'last_name', 'username': 'username'}
    data = users.objects.raw('SELECT * FROM myapp_users', translations=name_map)
    print(data)
    for p in data:
        print(p)
    context= {"status":"400"}
    return JsonResponse(context,status=400)
from multiprocessing import context
from django.shortcuts import render

# Create your views here.

from itertools import product
from django import http
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import users,orders,items
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



import json
global global_username
global is_admin



#global_username = None
def index(request):
    return redirect('loginpage')
    # return HttpResponse("empty path")

def loginpage(request):
    return render(request,"login.html")


def logout(requst):
    global global_username 
    global_username = ''
    global is_admin
    is_admin = False
    return redirect('loginpage')
    

# Create your views here.
def login(request):
    input_username = request.POST['input_username']
    input_password = request.POST['input_password']
    user = authenticate(request, username=input_username, password=input_password)
    if user is not None:
        login(request, user)
        
   
    # #print("test",json.dumps(users.objects.values()))
    # #print("input_username",input_username)
   

    # # match_email = list(users.objects.filter(username =input_username))
    # # print(match_email)
    # #print("comparing email from login ",match_email)
    # filtered_data = list(users.objects.filter(username= input_username))
    # #print(filtered_data[0].password)
        
    # if len(filtered_data) > 0:
    #     #print("filtered data :-", filtered_data)
    #     if input_password == filtered_data[0].password:
    #         #return HttpResponse("login successfull")
    #         # passed_massage = {"massage": " sucessfully login"}
    #         # return render(request,"login.html",passed_massage)
            
            
    #         # get_user_data = users.objects.filter(username = input_username).values()
    #         # get_items = items.objects.all()
    #         # get_ordered = orders.objects.filter(username = input_username).values()
            
    #         # print(get_ordered)
            
    #         # user_data ={"data": get_user_data}
    #         # item_data = {"item": get_items}
    #         # orders1 ={"order": get_ordered}
            
            
    #         # context = {"user_data": user_data,"item_data": item_data,"orders1": orders1}
    #         #global global_username
    #         global global_username
    #         global_username = input_username
                        
    #         return redirect('loggedin')
    #         # return render(request,"product&profile.html",context)

    #     else: 
    #         passed_massage = {"massage": " wrong password"}
    #         return render(request,"login.html",passed_massage)
    # else:
    #     #return HttpResponse(" wrong email ")
    #     passed_massage = {"massage": " invalid username "}
    #     return render(request,"login.html",passed_massage)
    #     # return redirect(request.META['HTTP_REFERER'],passed_massage)
        
        

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
            passed_massage = {"massage": "sign up success , please login "}      
            return render(request,"login.html",passed_massage)
            # return redirect(request.META['HTTP_REFERER'],passed_massage)
    
    
def loggedin(request):
    
    #place_order = items.objects.filter(name=product_name)
    global global_username 
    if not global_username:
        return redirect ("loginpage")
    
    get_user_data = users.objects.filter(username = global_username).values()
    get_items = items.objects.all()
    
    
    get_ordered = orders.objects.filter(username = global_username).exclude(status='cart').values()
    
    
    user_data ={"data": get_user_data}
    item_data = {"item": get_items}
    orders1 ={"order": get_ordered}
    
    
    context = {"user_data": user_data,"item_data": item_data,"orders1": orders1}
                
    return render(request,"product&profile.html",context)
    
            
            
def placeorder(request, id ):
    global global_username 
    if not global_username:
        return redirect ("loginpage")
    
    print(global_username)
    orders.objects.filter(oreder_id = id ).update(orderid=3, status ="unverified")
    #input_data 
    
    #place_order = items.objects.filter(name=product_name)
    
    # get_user_data = users.objects.filter(username = global_username).values()
    # get_items = items.objects.all()
    
    
    # get_ordered = orders.objects.filter(username = global_username).values()
    
    
    # user_data ={"data": get_user_data}
    # item_data = {"item": get_items}
    # orders1 ={"order": get_ordered}
    
    
    # context = {"user_data": user_data,"item_data": item_data,"orders1": orders1}
                
    #return render(request,"product&profile.html",context)
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
    
    


# def load_cart(request):
#     get_user_data = users.objects.filter(username = global_username).values()
#     get_ordered = orders.objects.filter(username= global_username, status = "cart").values()
    
#     user_data ={"data": get_user_data}
#     orders1 ={"order": get_ordered}
#     context = {"user_data": user_data,"orders1": orders1}
                
#     return render(request,"user_cart.html",context)
    
##
## user functions 
##

def add_to_cart(request, item_name, item_price, user_address):
    global global_username
    if not global_username:
        return redirect ("loginpage")
    
    print("add to cart running ")
    orders_obj = orders(username = global_username, orderid = 0, item = item_name, price = item_price, status="cart", address=user_address)
    orders_obj.save()
    return redirect(request.META["HTTP_REFERER"])
    #return redirect("user_cart_details")



def delete_from_cart(request , item_order_id):
    global global_username
    if not global_username:
        return redirect ("loginpage")
    
    orders_db_obj = orders.objects.filter(oreder_id = item_order_id).delete()
    #orders_db_obj.delete()
    #orders_db_obj.save()
    return redirect (request.META['HTTP_REFERER'])



def user_cart_details(request):
    global global_username
    if not global_username:
        return redirect ("loginpage")
    
    print("user cart running ")
    orders_in_cart = orders.objects.filter(status = "cart",username = global_username).values()
    get_user_data = users.objects.filter(username = global_username).values()
    orders_in_cart_deatils ={"orders": orders_in_cart}
    user_data ={"data": get_user_data}
    
    context = {"cart_datails":orders_in_cart_deatils, "user_data": user_data}
    
    return render(request, "user_cart.html", context)


def user_placed_orders(request):
    global global_username
    if not global_username:
        return redirect ("loginpage")
    
    get_user_data = users.objects.filter(username = global_username).values()
    get_ordered = orders.objects.filter(username= global_username).exclude(status = "cart").values()
    
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
    global global_username
    if not global_username:
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
    
    get_items = items.objects.all().values()
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
    global global_username
    if not global_username:
        return redirect ("loginpage")
    
    print(" confirm order called ")
    database_obj = orders.objects.get(oreder_id = id)
    print(database_obj.status)
    database_obj.status = 'confirmed'
    database_obj.save()
    return redirect (request.META['HTTP_REFERER'])



def decline_order(request, id):
    global global_username
    if not global_username:
        return redirect ("loginpage")
    
    print(" decline order called ")
    database_obj = orders.objects.get(oreder_id = id)
    print(database_obj.status)
    database_obj.status = 'declined'
    database_obj.save()
    return redirect (request.META['HTTP_REFERER'])


def change_status(request, id, new_status):
    # global global_username
    # if not global_username:
    #     return redirect ("loginpage")
    
    print("change status called ")
    database_obj = orders.objects.get(oreder_id = id)
    # print(database_obj.status)
    # print(new_status)
    database_obj.status = new_status
    database_obj.save()
    return redirect (request.META['HTTP_REFERER'])


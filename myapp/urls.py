from django.contrib import admin
from django.urls import path
import myapp
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from myapp import views


urlpatterns = [
    path("", views.index, name='index'),
    path("userlogin/",views.loginpage, name='userlogin'),
    path("loginpage", views.loginpage, name="loginpage"),
    path("login", views.login, name='login'),
    path("signup",views.signup, name='signup'),
    path("logout/", views.logout , name="logout"),
    
    path("loggedin",views.loggedin, name='loggedin'),
    path("placeorder/<int:id>/",views.placeorder, name='placeorder'),
    
    path("cart_details/", views.user_cart_details, name="user_cart_datials"),
    path("add_to_cart/<str:item_name>/<str:item_price>/<str:user_address>/", views.add_to_cart, name="add_to_cart"),
    path("delete_from_cart/<int:item_order_id>", views.delete_from_cart, name="delete_from_cart"),
    path("user_cart_details", views.user_cart_details, name="user_cart_details"),
    path("cancel_order/<int:id>", views.cancel_order, name="cancel_order"),
    
    
    path("admin_login/", views.admin_login, name="admin_login"),
    path("admin_login/change_status/<int:id>/<str:new_status>/" , views.change_status, name="change_status"),
    path("op_login", views.op_login, name="op_login"),
    
    path("order_manage", views.order_manage, name = 'order_manage'),
    path("confirm_order/<str:username>/<str:item>/<int:id>/", views.confirm_order, name='confirm_order'),
    path("decline_order/<int:id>/", views.decline_order, name='decline_order'),
    path("change_status/<int:id>/<str:new_status>/" , views.change_status, name="change_status"),
    
    path("order_processor_login/", views.order_processor_login),
    path("user_placed_orders/", views.user_placed_orders, name='user_placed_orders'),
    path("order_all/<str:passed_username>/", views.orderall, name="order_all"),
    
    path("manage_items/", views.manage_items, name="manage_items"),
    path("manage_items/add_item/", views.add_item, name="add_item"),
    path("manage_items/delete_item/<str:item_name>/", views.delete_item, name="delete_item"),
    
    path("images/", views.images, name="images"),
    path("user_profile/", views.user_profile, name="user_profile"),
    path("practice_raw/", views.practice_raw, name="practice_raw")
    
    
]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
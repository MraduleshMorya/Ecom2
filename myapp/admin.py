from django.contrib import admin

# Register your models here.
from django.contrib import admin

from myapp.models import items, orders, users,new_orders,image_db

# Register your models here.

admin.site.register(users)
admin.site.register(items)
admin.site.register(orders)
admin.site.register(new_orders)
admin.site.register(image_db)



from dataclasses import Field
from sys import maxsize
from typing_extensions import Required
from django.db import models
from django.forms import ImageField

# Create your models here.

# class Name(models.Model):
    

#     def __str__(self):
#         return 

#     def __unicode__(self):
#         return 


# class NameAdmin(admin.ModelAdmin):
#     list_display = ('',)

# admin.site.register(Name, NameAdmin)

class users(models.Model):
    username = models.CharField(max_length=20, primary_key=True) 
    password = models.CharField(max_length=10)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    address = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=10, default="1234567890")
    
    def __str__(self):
        return self.username
    
    
    
class items(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.name
    

class orders(models.Model):
    oreder_id= models.AutoField(primary_key=True)
    orderid= models.IntegerField()
    username = models.CharField(max_length=20)
    item = models.CharField(max_length=20)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default='confirmation pending')
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username
    
    
class new_orders(models.Model):
    oreder_id= models.AutoField(primary_key=True)
    orderid= models.IntegerField()
    username = models.CharField(max_length=20)
    item = models.CharField(max_length=20)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default='confirmation pending')
    
    def __str__(self):
        return self.username
    
    
class image_db(models.Model):
    images = models.ImageField(upload_to='images/')
    
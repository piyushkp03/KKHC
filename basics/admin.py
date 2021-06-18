from django.contrib import admin
from .models import Products,medicines,usercart,orders

# Register your models here.
admin.site.register(Products)
admin.site.register(medicines)
admin.site.register(usercart)
admin.site.register(orders)
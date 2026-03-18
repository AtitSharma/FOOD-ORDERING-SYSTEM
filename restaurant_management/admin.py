from django.contrib import admin

# Register your models here.
from restaurant_management.models import *

admin.site.register({
    Category,Food,TableOrder,TableOrderItem,Table,FoodImage,Cart
})
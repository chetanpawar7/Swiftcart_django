from django.contrib import admin
from .models import Customer,Product,Cart,Order


# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cart,CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order,OrderAdmin)



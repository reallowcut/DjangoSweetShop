from django.contrib import admin
from shop.models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

from django.contrib.auth import login
from django.urls import path
from . import views
from .views import *

app_name = 'shop'
urlpatterns = [
    path('', views.categories, name='categories'),
    path('baskets/', views.basket_page, name='basket_page'),
    path('baskets/add/<slug:product_slug>/', views.basket_add, name='basket_add'),
    path('baskets/drop/<slug:product_slug>/', views.basket_drop, name='basket_drop'),
    path('baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
    path('baskets/basket_complete', views.basket_complete, name='basket_complete'),
    # path('<int:category_id>', views.products_of_category, name='products_of_category')
    path('<slug:category_slug>/', views.products_of_category, name='products_of_category'),
    path('<slug:category_slug>/page/<int:page_number>/', views.products_of_category, name='paginator'),

]

import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from shop.forms import OrderForm
from shop.models import *
from django.core.paginator import Paginator


def products_of_category(request, category_slug, page_number=1):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()

    per_page = 6
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)

    context = {'products': products_paginator,
               'category_now': category,
               'categories': categories}
    return render(request, 'shop/products_of_category.html', context)


def product_description(request, category_slug ,product_slug):
    product = Product.objects.get(slug=product_slug)

    context = {'product': product}
    return render(request, 'shop/product_description.html', context)

def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'shop/categories.html', context)


def basket_page(request):
    if request.method == 'post':
        return render(request, 'shop/basket_complete.html')

    baskets = Basket.objects.filter(user=request.user)

    form = OrderForm()

    total_sum = sum(basket.sum() for basket in baskets)
    total_quantity = sum(basket.quantity for basket in baskets)

    context = {'baskets': baskets,
               'total_sum': total_sum,
               'total_quantity': total_quantity,
               'form': form}
    return render(request, 'shop/baskets.html', context)


@login_required
def basket_complete(request):
    now = datetime.datetime.now()
    hour_now = now.hour

    if 8 < hour_now < 22:
        return render(request, 'shop/basket_complete.html')
    else:
        return render(request, 'shop/closed_section.html')


@login_required
def basket_add(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        if basket.quantity >= 50:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        basket.quantity = basket.quantity + 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_drop(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        if basket.quantity == 0:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        basket.quantity = basket.quantity - 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

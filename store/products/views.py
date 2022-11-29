from django.http import HttpResponseRedirect
from django.shortcuts import render
from products.models import Product, ProductCategory, Basket


def index(request):
    context = {'title': 'Store'}
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Store - товары',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'products/products.html', context)


def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)

    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = basket.last()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

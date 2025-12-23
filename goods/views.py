from django.shortcuts import render

from .models import Products, Categories


def catalog(request):

    goods = Products.objects.all()

    context = {
        'title': 'Home - Каталог',
        'goods': goods
    }

    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):

    product = Products.objects.get(slug=product_slug)

    context = {
        'title': 'Home - Certain product',
        'product': product
    }

    return render(request, 'goods/product.html', context)
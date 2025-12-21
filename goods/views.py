from django.shortcuts import render


def catalog(request):
    return render(request, 'goods/catalgo.html')


def product(request):
    return render(request, 'goods/product.html')
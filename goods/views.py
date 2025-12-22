from django.shortcuts import render



def catalog(request):

    context = {
        'title': 'Home - Каталог',
    }

    return render(request, 'goods/catalog.html')


def product(request):
    context = {
        'title': '',
    }

    return render(request, 'goods/product.html')
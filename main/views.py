from django.shortcuts import render

from goods.models import Categories


def index(request):

    categories = Categories.objects.all()

    context = {
        'title': 'Home - Main page',
        'content': 'Магазин мебели HOME',

        'categories': categories
    }

    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Home - About page',
        'content': 'О нас'
    }

    return render(request, 'main/about.html', context)


def contact(request):
    context = {
        'title': 'Home - Contact page',
        'content': 'Контактная инфо'
    }

    return render(request, 'main/contact.html', context)
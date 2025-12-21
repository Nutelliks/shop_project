from django.shortcuts import render


def index(request):
    context = {
        'title': 'Home - Main page'
    }
    render(request, 'main/index.html', context)
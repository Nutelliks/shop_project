from typing import Any

from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Main page"
        context["content"] = "Магазин мебели HOME"
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - About page"
        context["content"] = "О нас"
        return context
    

class ContactView(TemplateView):
    template_name = 'main/contact.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Contact page"
        context["content"] = "Контактная инфо"
        return context
    

# def index(request):

#     context = {
#         'title': 'Home - Main page',
#         'content': 'Магазин мебели HOME',
#     }

#     return render(request, 'main/index.html', context)


# def about(request):
#     context = {
#         'title': 'Home - About page',
#         'content': 'О нас'
#     }

#     return render(request, 'main/about.html', context)


# def contact(request):
#     context = {
#         'title': 'Home - Contact page',
#         'content': 'Контактная инфо'
#     }

#     return render(request, 'main/contact.html', context)
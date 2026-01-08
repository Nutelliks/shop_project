from django.urls import path
from django.views.decorators.cache import cache_page

from . import views


app_name = 'main'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', cache_page(30)(views.ContactView.as_view()), name='contact'),  # King of caching: via url path

]

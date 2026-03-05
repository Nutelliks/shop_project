from django.urls import path
from .api.views import CategoryListAPIView

from . import views


app_name = 'catalog'
urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),

    path('api/categories/', CategoryListAPIView.as_view(), name='api_category')
]

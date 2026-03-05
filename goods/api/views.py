from rest_framework import generics
from ..models import Categories
from .serializers import CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    """API для получения всех корневых категорий с их деревом."""
    serializer_class = CategorySerializer
    queryset = Categories.objects.filter(parent__isnull=True, is_active=True)
    # parent__isnull=True - только корневые категории


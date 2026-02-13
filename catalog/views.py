from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryListView(generics.ListAPIView):
    """Эндпоинт для просмотра всех категорий с подкатегориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardPagination

class ProductListView(generics.ListAPIView):
    """Эндпоинт для просмотра всех продуктов с пагинацией"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardPagination
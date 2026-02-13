from rest_framework import serializers
from .models import Category, SubCategory, Product

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'image']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'subcategories']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='subcategory.category.name', read_only=True)
    subcategory = serializers.CharField(source='subcategory.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'slug', 
            'category', 
            'subcategory', 
            'price', 
            'image_original'
        ]
from rest_framework import serializers
from .models import Category, SubCategory, Product, Cart, CartItem

class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегорий"""
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'image']

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий с вложенными подкатегориями"""
    subcategories = SubCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'subcategories']

class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов"""
    category = serializers.CharField(source='subcategory.category.name', read_only=True)
    subcategory = serializers.CharField(source='subcategory.name', read_only=True)
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'slug', 
            'category', 
            'subcategory', 
            'price', 
            'images'
        ]
    
    def get_images(self, obj):
        """Возвращает словарь со всеми изображениями товара"""
        return obj.images_list

class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор для товара в корзине"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    total_price = serializers.SerializerMethodField()
    product_images = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'product_images', 'quantity', 'total_price', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_total_price(self, obj):
        """Общая стоимость товара в корзине"""
        return obj.product.price * obj.quantity
    
    def get_product_images(self, obj):
        """Изображения товара"""
        return obj.product.images_list

class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины"""
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'username', 'items', 'total_price', 'total_items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_total_price(self, obj):
        """Общая стоимость всех товаров в корзине"""
        return sum(item.product.price * item.quantity for item in obj.items.all())
    
    def get_total_items(self, obj):
        """Общее количество товаров в корзине"""
        return sum(item.quantity for item in obj.items.all())

class AddToCartSerializer(serializers.Serializer):
    """Сериализатор для добавления товара в корзину"""
    product_id = serializers.IntegerField(
        required=True,
        help_text="ID товара"
    )
    quantity = serializers.IntegerField(
        required=False,
        default=1,
        min_value=1,
        help_text="Количество товара (минимум 1)"
    )    

class UpdateCartItemSerializer(serializers.Serializer):
    """Сериализатор для изменения количества товара"""
    quantity = serializers.IntegerField(min_value=0)
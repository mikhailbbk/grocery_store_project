from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .models import Category, Product, Cart, CartItem
from .serializers import (
    CategorySerializer, ProductSerializer, CartSerializer,
    AddToCartSerializer, UpdateCartItemSerializer
)

def home(request):
    """Главная страница с ссылками на все эндпоинты"""
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Grocery Store API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #34495e;
                margin-top: 30px;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .section {
                background: #f8f9fa;
                border-left: 4px solid #3498db;
                padding: 15px;
                margin: 20px 0;
                border-radius: 0 8px 8px 0;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
                padding: 10px;
                background: white;
                border-radius: 5px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                display: flex;
                align-items: center;
                flex-wrap: wrap;
            }
            a {
                color: #3498db;
                text-decoration: none;
                font-weight: 500;
            }
            a:hover {
                color: #2980b9;
                text-decoration: underline;
            }
            .method {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 12px;
                margin-right: 10px;
                min-width: 50px;
                text-align: center;
            }
            .get { background: #61affe; color: white; }
            .post { background: #49cc90; color: white; }
            .put { background: #fca130; color: white; }
            .delete { background: #f93e3e; color: white; }
            .url {
                font-family: monospace;
                background: #ecf0f1;
                padding: 5px;
                border-radius: 3px;
                margin-right: 10px;
            }
            .badge {
                background: #3498db;
                color: white;
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 12px;
                margin-left: 10px;
            }
            .warning {
                background: #fff3cd;
                color: #856404;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                border: 1px solid #ffeeba;
                margin-top: 15px;
            }
            .swagger-section-link {
                display: inline-block;
                background: #6c5ce7;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                text-decoration: none;
                font-size: 16px;
                margin-top: 10px;
                margin-bottom: 10px;
                transition: background 0.3s;
                font-weight: bold;
            }
            .swagger-section-link:hover {
                background: #5649c0;
                color: white;
                text-decoration: none;
            }
            .token-demo {
                background: #2c3e50;
                color: #ecf0f1;
                padding: 10px;
                border-radius: 5px;
                font-family: monospace;
                margin-top: 15px;
            }
            .endpoint-list {
                margin-top: 15px;
            }
            .section-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
            }
            footer {
                margin-top: 40px;
                text-align: center;
                color: #7f8c8d;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Grocery Store API</h1>
            <p>Добро пожаловать в API магазина продуктов. Ниже представлены все доступные эндпоинты.</p>
            
            <div class="section">
                <h2>Документация</h2>
                <ul>
                    <li>
                        <span class="method get">GET</span>
                        <a href="/swagger/" target="_blank" class="url">/swagger/</a>
                        <span class="badge">Интерактивная документация</span>
                    </li>
                    <li>
                        <span class="method get">GET</span>
                        <a href="/redoc/" target="_blank" class="url">/redoc/</a>
                        <span class="badge">Альтернативная документация</span>
                    </li>
                </ul>
            </div>

            <div class="section">
                <h2>Публичные эндпоинты (GET запросы)</h2>
                <ul>
                    <li>
                        <span class="method get">GET</span>
                        <a href="/api/categories/" target="_blank" class="url">/api/categories/</a>
                        <span> - список категорий с подкатегориями</span>
                    </li>
                    <li>
                        <span class="method get">GET</span>
                        <a href="/api/products/" target="_blank" class="url">/api/products/</a>
                        <span> - список товаров</span>
                    </li>
                </ul>
            </div>

            <div class="section">
                <h2>Авторизация</h2>
                <ul>
                    <li>
                        <span class="method post">POST</span>
                        <span class="url">/api/login/</span>
                        <span> - получение токена (username/password)</span>
                        <a href="/swagger/#/login/login_create" target="_blank" class="swagger-link" style="background: #6c5ce7; color: white; padding: 5px 15px; border-radius: 5px; text-decoration: none; font-size: 14px; margin-left: 15px;">Тестировать в Swagger →</a>
                    </li>
                </ul>
                <div class="token-demo">
                    <strong>Пример получения токена:</strong><br>
                    curl -X POST http://127.0.0.1:8000/api/login/ -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin123"}'
                </div>
            </div>

            <div class="section">
                <div class="section-header">
                    <h2>Корзина (требуется токен)</h2>
                    <a href="/swagger/#/cart" target="_blank" class="swagger-section-link">Тестировать все эндпоинты корзины в Swagger →</a>
                </div>
                
                <div class="endpoint-list">
                    <ul>
                        <li>
                            <span class="method get">GET</span>
                            <span class="url">/api/cart/</span>
                            <span> - просмотр корзины</span>
                        </li>
                        <li>
                            <span class="method post">POST</span>
                            <span class="url">/api/cart/add/</span>
                            <span> - добавить товар</span>
                        </li>
                        <li>
                            <span class="method put">PUT</span>
                            <span class="url">/api/cart/item/{id}/</span>
                            <span> - изменить количество</span>
                        </li>
                        <li>
                            <span class="method delete">DELETE</span>
                            <span class="url">/api/cart/item/{id}/remove/</span>
                            <span> - удалить товар</span>
                        </li>
                        <li>
                            <span class="method delete">DELETE</span>
                            <span class="url">/api/cart/clear/</span>
                            <span> - очистить корзину</span>
                        </li>
                    </ul>
                </div>

                <div class="warning">
                    <strong>Важно:</strong> Для тестирования корзины необходимо:
                    <ol style="margin-top: 5px; margin-bottom: 0;">
                        <li>Получить токен через <code>/api/login/</code></li>
                        <li>Нажать кнопку <strong>"Authorize"</strong> в Swagger</li>
                        <li>Ввести токен в формате: <code>Token ваш_токен</code></li>
                    </ol>
                </div>
            </div>

            <div class="section">
                <h2>Администрирование</h2>
                <ul>
                    <li>
                        <span class="method get">GET</span>
                        <a href="/admin/" target="_blank" class="url">/admin/</a>
                        <span> - админ панель</span>
                    </li>
                </ul>
            </div>

            <footer>
                <p>Grocery Store API v1.0 | Разработано для тестового задания</p>
                <p><strong>Тестовый пользователь:</strong> admin / admin123</p>
            </footer>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


class StandardPagination(PageNumberPagination):
    """Пагинация для API"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryListView(generics.ListAPIView):
    """Эндпоинт для просмотра всех категорий с подкатегориями"""
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardPagination


class ProductListView(generics.ListAPIView):
    """Эндпоинт для просмотра всех продуктов с пагинацией"""
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardPagination


class LoginView(ObtainAuthToken):
    """Эндпоинт для получения токена авторизации"""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


class CartView(generics.RetrieveAPIView):
    """Эндпоинт для просмотра корзины с подсчетом количества и суммы"""
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    
    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(generics.CreateAPIView):
    """Эндпоинт для добавления товара в корзину"""
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = get_object_or_404(Product, id=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class UpdateCartItemView(generics.UpdateAPIView):
    """Эндпоинт для изменения количества товара в корзине"""
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCartItemSerializer
    
    def get_object(self):
        cart = get_object_or_404(Cart, user=self.request.user)
        return get_object_or_404(CartItem, cart=cart, id=self.kwargs['item_id'])
    
    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        quantity = serializer.validated_data['quantity']
        
        if quantity == 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        cart = get_object_or_404(Cart, user=request.user)
        return Response(CartSerializer(cart).data)


class RemoveFromCartView(generics.DestroyAPIView):
    """Эндпоинт для удаления товара из корзины"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        cart = get_object_or_404(Cart, user=self.request.user)
        return get_object_or_404(CartItem, cart=cart, id=self.kwargs['item_id'])
    
    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        cart = get_object_or_404(Cart, user=request.user)
        return Response(CartSerializer(cart).data)


class ClearCartView(generics.DestroyAPIView):
    """Эндпоинт для полной очистки корзины"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        cart = self.get_object()
        cart.items.all().delete()
        return Response(
            {"message": "Корзина успешно очищена", "cart": CartSerializer(cart).data}, 
            status=status.HTTP_200_OK
        )
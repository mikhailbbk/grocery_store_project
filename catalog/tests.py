from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, SubCategory, Product, Cart, CartItem

class CategoryAPITestCase(TestCase):
    """Тесты для API категорий"""
    
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Тестовая категория",
            slug="test-category"
        )
        self.subcategory = SubCategory.objects.create(
            name="Тестовая подкатегория",
            slug="test-subcategory",
            category=self.category
        )
    
    def test_get_categories(self):
        """Тест GET запроса к /api/categories/"""
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Тестовая категория")
        self.assertEqual(len(response.data['results'][0]['subcategories']), 1)


class ProductAPITestCase(TestCase):
    """Тесты для API продуктов"""
    
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Тестовая категория",
            slug="test-category"
        )
        self.subcategory = SubCategory.objects.create(
            name="Тестовая подкатегория",
            slug="test-subcategory",
            category=self.category
        )
        self.product = Product.objects.create(
            name="Тестовый продукт",
            slug="test-product",
            price=100.00,
            subcategory=self.subcategory
        )
    
    def test_get_products(self):
        """Тест GET запроса к /api/products/"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Тестовый продукт")
        self.assertEqual(response.data['results'][0]['price'], "100.00")
    
    def test_get_products_pagination(self):
        """Тест пагинации продуктов"""        
        for i in range(15):
            Product.objects.create(
                name=f"Тестовый продукт {i}",
                slug=f"test-product-{i}",
                price=100.00 + i,
                subcategory=self.subcategory
            )
        
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])


class CartAPITestCase(TestCase):
    """Тесты для API корзины"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Тестовая категория",
            slug="test-category"
        )
        self.subcategory = SubCategory.objects.create(
            name="Тестовая подкатегория",
            slug="test-subcategory",
            category=self.category
        )
        self.product = Product.objects.create(
            name="Тестовый продукт",
            slug="test-product",
            price=100.00,
            subcategory=self.subcategory
        )
    
    def test_login_post(self):
        """Тест POST запроса к /api/login/ (получение токена)"""
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_add_to_cart_without_auth(self):
        """Тест добавления в корзину без авторизации (должен быть 401)"""
        data = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post('/api/cart/add/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_add_to_cart_with_auth(self):
        """Тест добавления в корзину с авторизацией"""        
        login_response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        token = login_response.data['token']        
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')        
        
        data = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post('/api/cart/add/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_items'], 2)
        self.assertEqual(float(response.data['total_price']), 200.00)
    
    def test_view_cart(self):
        """Тест просмотра корзины"""        
        login_response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')        
        
        self.client.post('/api/cart/add/', {
            'product_id': self.product.id, 
            'quantity': 3
        })        
        
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_items'], 3)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], "Тестовый продукт")
    
    def test_update_cart_item(self):
        """Тест изменения количества товара"""        
        login_response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')        
        
        self.client.post('/api/cart/add/', {
            'product_id': self.product.id, 
            'quantity': 2
        })        
        
        cart = self.client.get('/api/cart/').data
        item_id = cart['items'][0]['id']        
        
        response = self.client.put(f'/api/cart/item/{item_id}/', {
            'quantity': 5
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_items'], 5)
    
    def test_clear_cart(self):
        """Тест очистки корзины"""        
        login_response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')        
        
        self.client.post('/api/cart/add/', {
            'product_id': self.product.id, 
            'quantity': 3
        })        
        
        response = self.client.delete('/api/cart/clear/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        
        cart_response = self.client.get('/api/cart/')
        self.assertEqual(cart_response.data['total_items'], 0)
from django.urls import path
from . import views

urlpatterns = [
    # Публичные эндпоинты (доступны всем)
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    
    # Авторизация
    path('login/', views.LoginView.as_view(), name='login'),
    
    # Эндпоинты корзины (только для авторизованных)
    path('cart/', views.CartView.as_view(), name='cart-detail'),
    path('cart/add/', views.AddToCartView.as_view(), name='cart-add'),
    path('cart/item/<int:item_id>/', views.UpdateCartItemView.as_view(), name='cart-item-update'),
    path('cart/item/<int:item_id>/remove/', views.RemoveFromCartView.as_view(), name='cart-item-remove'),
    path('cart/clear/', views.ClearCartView.as_view(), name='cart-clear'),
]
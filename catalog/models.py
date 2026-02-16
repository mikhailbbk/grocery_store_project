from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator, MinValueValidator
from django.conf import settings
from PIL import Image
import os

def category_image_path(instance, filename):
    """Генерирует путь для сохранения изображения категории"""
    return f'categories/{instance.slug}/{filename}'

def subcategory_image_path(instance, filename):
    """Генерирует путь для сохранения изображения подкатегории"""
    return f'subcategories/{instance.slug}/{filename}'

def product_image_path(instance, filename):
    """Генерирует путь для сохранения изображений продукта"""
    # Получаем расширение файла
    ext = filename.split('.')[-1].lower()
    # Создаем имя файла с размером
    filename = f"{instance.slug}_original.{ext}"
    return f'products/{instance.slug}/{filename}'

class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(
        max_length=200, 
        verbose_name='Наименование',
        validators=[MinLengthValidator(3)]
    )
    slug = models.SlugField(
        max_length=250, 
        unique=True, 
        verbose_name='Slug',
        help_text='Уникальный идентификатор для URL'
    )
    image = models.ImageField(
        upload_to=category_image_path,
        verbose_name='Изображение',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    """Модель подкатегории товаров"""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )
    name = models.CharField(
        max_length=200, 
        verbose_name='Наименование',
        validators=[MinLengthValidator(3)]
    )
    slug = models.SlugField(
        max_length=250, 
        unique=True, 
        verbose_name='Slug',
        help_text='Уникальный идентификатор для URL'
    )
    image = models.ImageField(
        upload_to=subcategory_image_path,
        verbose_name='Изображение',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['category', 'name']
        unique_together = ['category', 'slug']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while SubCategory.objects.filter(category=self.category, slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Product(models.Model):
    """Модель товара"""
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Подкатегория'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование',
        validators=[MinLengthValidator(3)]
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name='Slug',
        help_text='Уникальный идентификатор для URL'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
        validators=[MinValueValidator(0)]
    )
    
    # Изображения в трех размерах
    image_original = models.ImageField(
        upload_to=product_image_path,
        verbose_name='Оригинальное изображение',
        blank=True,
        null=True
    )
    image_large = models.ImageField(
        upload_to=product_image_path,
        verbose_name='Большое изображение (800x800)',
        blank=True,
        null=True,
        editable=False
    )
    image_medium = models.ImageField(
        upload_to=product_image_path,
        verbose_name='Среднее изображение (400x400)',
        blank=True,
        null=True,
        editable=False
    )
    image_small = models.ImageField(
        upload_to=product_image_path,
        verbose_name='Маленькое изображение (200x200)',
        blank=True,
        null=True,
        editable=False
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Переопределенный save для создания трех размеров изображения"""
        if not self.slug:
            self.slug = slugify(self.name)        
        
        super().save(*args, **kwargs)        
        
        if self.image_original and not self.image_small:
            self.create_image_sizes()            
            super().save(*args, **kwargs)
    
    def create_image_sizes(self):
        """Создает три размера изображения из оригинального"""
        if not self.image_original:
            return
        
        try:            
            img = Image.open(self.image_original.path)            
            
            base_path = self.image_original.path
            base_name = os.path.basename(base_path)
            base_dir = os.path.dirname(base_path)
            name_without_ext = os.path.splitext(base_name)[0].replace('_original', '')
            ext = os.path.splitext(base_name)[1]
                        
            os.makedirs(base_dir, exist_ok=True)
            
            # Размеры для ресайза
            sizes = {
                'large': (800, 800),
                'medium': (400, 400),
                'small': (200, 200)
            }            
            
            for size_name, (width, height) in sizes.items():                
                img_copy = img.copy()                
                
                img_copy.thumbnail((width, height), Image.Resampling.LANCZOS)                
                
                new_filename = f"{name_without_ext}_{size_name}{ext}"
                new_path = os.path.join(base_dir, new_filename)                
                
                img_copy.save(new_path)                
                
                relative_path = os.path.relpath(new_path, settings.MEDIA_ROOT).replace('\\', '/')
                if size_name == 'large':
                    self.image_large.name = relative_path
                elif size_name == 'medium':
                    self.image_medium.name = relative_path
                elif size_name == 'small':
                    self.image_small.name = relative_path
                    
        except Exception as e:
            print(f"Ошибка при создании изображений: {e}")
    
    @property
    def category(self):
        """Возвращает категорию товара через подкатегорию"""
        return self.subcategory.category
    
    @property
    def images_list(self):
        """Возвращает словарь со всеми изображениями товара"""
        images = {}
        if self.image_small:
            images['small'] = self.image_small.url
        if self.image_medium:
            images['medium'] = self.image_medium.url
        if self.image_large:
            images['large'] = self.image_large.url
        if self.image_original:
            images['original'] = self.image_original.url
        return images


class Cart(models.Model):
    """Модель корзины пользователя"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        return f"Корзина {self.user.username}"
    
    @property
    def total_price(self):
        """Общая стоимость всех товаров в корзине"""
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_items(self):
        """Общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Модель товара в корзине"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    @property
    def total_price(self):
        """Стоимость товара в корзине"""
        return self.product.price * self.quantity
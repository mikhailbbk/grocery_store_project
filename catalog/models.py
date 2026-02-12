from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator, MinValueValidator
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
    ext = filename.split('.')[-1]
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
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def category(self):
        """Возвращает категорию товара через подкатегорию"""
        return self.subcategory.category
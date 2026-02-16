# Grocery Store API

Тестовое задание для стажировки. API для магазина продуктов с корзиной и авторизацией.

## Быстрый старт

```bash
# 1. Клонировать
git clone <repository-url>
cd grocery_store_project

# 2. Виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Зависимости
pip install -r requirements.txt

# 4. Миграции
python manage.py migrate

# 5. Фикстуры (тестовые данные)
python manage.py loaddata catalog/fixtures/*.json

# 6. Суперпользователь
python manage.py createsuperuser

# 7. Запуск
python manage.py runserver
```

## Реализованный функционал

-   **Категории и подкатегории (админка + API)**
-   **Товары с 3 размерами изображений**
-   **Пагинация для списков**
-   **Токен-авторизация (/api/login/)**
-   **Корзина (добавление, изменение, удаление, очистка)**
-   **Подсчет суммы и количества в корзине**
-   **Swagger документация**
-   **9 автотестов (GET/POST)**
-   **Фикстуры с тестовыми данными**

## Основные эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/categories/` | Категории + подкатегории |
| GET | `/api/products/` | Товары |
| POST | `/api/login/` | Получить токен |
| GET | `/api/cart/` | Моя корзина |
| POST | `/api/cart/add/` | Добавить товар |
| PUT | `/api/cart/item/{id}/` | Изменить количество |
| DELETE | `/api/cart/item/{id}/remove/` | Удалить товар |
| DELETE | `/api/cart/clear/` | Очистить корзину |

**Полная документация:** [`/swagger/`](http://127.0.0.1:8000/swagger/)

## Тестовый пользователь

-   **Логин: admin**
-   **Пароль: admin123**

## Запуск тестов

```bash
python manage.py test
```

# Фикстуры

-   **catalog/fixtures/categories.json**
-   **catalog/fixtures/subcategories.json**
-   **catalog/fixtures/products.json**

## Технологии

-   **Python 3.12**
-   **Django 6.0**
-   **Django REST Framework**
-   **SQLite**
-   **drf-yasg (Swagger)**

## Развитие проекта

-   **Регистрация пользователей** – эндпоинт для самостоятельного создания аккаунта
-   **Фильтрация и поиск товаров** – по цене, категории, названию
-   **Оформление заказов** – история покупок
-   **Rate limiting** – защита от брутфорса
-   **Срок действия токенов** – автоматическое истечение через 7 дней

## Контакты

-   **GitHub: mikhailbbk**
-   **Email: mikhailbbk.dev@gmail.com**
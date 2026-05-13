# Foodgram

Foodgram - это социальная сеть для обмена рецептами. Пользователи могут публиковать свои рецепты, подписываться на других пользователей, добавлять рецепты в избранное и создавать списки покупок.

## Fitnessgram (текущая версия репозитория)

Бэкенд переведён на **планы тренировок** (`/api/workout-plans/`) и **упражнения** (`/api/exercises/`). Старый фронт по-прежнему использует URL вида `/recipes/…`, но слой [`frontend/src/api/index.js`](frontend/src/api/index.js) проксирует запросы к новому API.

### Быстрый доступ (Postman / браузер)

| Что | Как |
|-----|-----|
| Токен | `POST /api/auth/token/login/` JSON: `{"email":"…","password":"…"}` → поле `auth_token` |
| Запросы с токеном | Заголовок `Authorization: Token <auth_token>` |
| Текущий пользователь | `GET /api/users/me/` |
| Список планов | `GET /api/workout-plans/?page=1&limit=6` (пагинация как в foodgram) |
| Избранное (фильтр) | `GET /api/workout-plans/?is_favorited=true` |
| Админка Django | `http://localhost/admin/` (или `http://localhost:8000/admin/` при прямом доступе к backend) |
| Вход в админку | **Email** (не username): `admin@example.com`, пароль: `admin` — создаётся при старте контейнера командой `create_superuser`, если пользователя ещё нет |

Переменные для CSRF за reverse-proxy при необходимости: `CSRF_TRUSTED_ORIGINS`, `USE_X_FORWARDED_HOST` (см. [`backend/foodgram/settings.py`](backend/foodgram/settings.py)).

## Технологии

### Backend
- Python 3.9+
- Django 3.2
- Django REST Framework
- PostgreSQL
- Docker
- Nginx

### Frontend
- React
- JavaScript
- HTML/CSS
- Docker
- Nginx

## Структура проекта

```
foodgram/
├── backend/               # Django backend приложение
│   ├── api/              # API endpoints и сериализаторы
│   ├── ingredient/       # Модели и логика для ингредиентов
│   ├── recipes/          # Модели и логика для рецептов
│   ├── users/            # Модели и логика для пользователей
│   ├── foodgram/         # Основные настройки Django проекта
│   ├── const/            # Константы и утилиты
│   ├── data/             # Данные для загрузки (ингредиенты)
│   ├── manage.py         # Django management script
│   └── requirements.txt  # Зависимости Python
├── frontend/             # React frontend приложение
├── infra/               # Docker и Nginx конфигурации
├── docs/                # Документация и скриншоты
│   └── screenshots/     # Скриншоты приложения
├── postman_collection/  # Postman коллекция для тестирования API
└── .github/             # GitHub Actions конфигурации
```

## Основные функции

- Регистрация и авторизация пользователей
- Создание, редактирование и удаление рецептов
- Подписка на других пользователей
- Добавление рецептов в избранное
- Создание списка покупок
- Фильтрация рецептов по тегам
- API для взаимодействия с приложением

## Установка и запуск

### Требования
- Docker
- Docker Compose

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/PinGBin74/foodgram-st.git
cd foodgram
```

2. Создайте файл .env в директории backend со следующими переменными:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

3. Перейти в папку frontend:
```bash
cd fronend
```

4. Выполнить две команды:
```bash
npm install --legacy-peer-deps
npm run build
```

5. Запустите проект с помощью Docker Compose:
```bash

cd .. && cd infra && docker-compose up --build
```


После этого проект будет доступен по адресу http://localhost/

## API Endpoints

API документация доступна по адресу http://localhost/api/docs/

Основные эндпоинты:
- `/api/users/` - управление пользователями
- `/api/recipes/` - управление рецептами
- `/api/ingredients/` - управление ингредиентами

## Скриншоты приложения

### Создание рецепта
![Создание рецепта](docs/screenshots/creating_recipe.png)
Интерфейс создания нового рецепта, где пользователь может указать название, описание, время приготовления, ингредиенты и шаги приготовления.

### Готовый рецепт
![Готовый рецепт](docs/screenshots/done_recipe.png)
Пример готового рецепта с полным описанием, списком ингредиентов и пошаговыми инструкциями.

### Редактирование рецепта
![Редактирование рецепта](docs/screenshots/changing_describtion.png)
Страница редактирования рецепта, позволяющая изменить все детали существующего рецепта.

### Список покупок
![Список покупок](docs/screenshots/shopping_list.png)
Интерфейс списка покупок, где пользователь может видеть все необходимые ингредиенты для выбранных рецептов.

### Экспорт списка покупок
![Экспорт списка покупок](docs/screenshots/csv_file.png)
Пример экспортированного списка покупок в формате CSV.


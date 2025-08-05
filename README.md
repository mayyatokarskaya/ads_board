# Ads Board (Доска объявлений)

Проект **Ads Board** — это веб-приложение для размещения и управления объявлениями, реализованное на базе **Django** и **Django REST Framework (DRF)**.

---

## 🔑 Ключевые особенности

- Django + DRF: реализация RESTful API
- Авторизация через JWT (djangorestframework-simplejwt)
- PostgreSQL через psycopg2-binary (без прямого SQL)
- Кастомная модель пользователя и разграничение прав (админ / пользователь)
- drf-spectacular — автоматическая генерация OpenAPI схемы и документации
- JWT-вход/обновление токена с аннотацией схемы
- Покрытие тестами >75% (pytest, coverage)
- Проверка стиля: flake8, black, isort
- Загрузка и хранение изображений к объявлениям
- Docker и Docker Compose для запуска
- ALLOWED_HOSTS и .env-конфигурация для продакшн-окружения

---

## 🧰 Стек технологий

- Python 3.13
- Django 5.2
- Django REST Framework 3.16
- PostgreSQL
- psycopg2-binary
- SimpleJWT (JWT авторизация)
- drf-spectacular (документация)
- Poetry (зависимости)
- Docker + Docker Compose
- pytest, pytest-django, coverage
- flake8, black, isort

---

## 🚀 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd ads-board
```

### 2. Создание .env

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
SECRET_KEY=ваш_секретный_ключ
DEBUG=True
DB_NAME=ads_board
DB_USER=ads_board_user
DB_PASSWORD=ads_board_password
DB_HOST=db
DB_PORT=5432
```

### 3. Установка зависимостей через Poetry

```bash
poetry install
```

### 4. Запуск с Docker

```bash
docker-compose down --volumes --remove-orphans
docker-compose build --no-cache
docker-compose up
```

### 5. Миграции и суперпользователь

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## 📡 Использование API

- OpenAPI schema: [/api/schema/](http://localhost:8000/api/schema/)
- Swagger UI: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- Redoc: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)

### JWT Авторизация

- Вход: `Вход: POST /api/token/login/` (email + password) (получение access и refresh токенов)
- Обновление токена: `POST /api/token/refresh/`

### Основные эндпоинты:

- `/api/ads/` — CRUD объявлений
- `/api/auth/` — JWT авторизация

---

## 📁 Структура проекта

```bash
ads-board/
├── ads/                  # Приложение объявлений
│   ├── models.py
│   ├── serializers.py
│   └── urls.py
├── users/                # Приложение пользователей
│   ├── models.py
│   ├── serializers.py
│   ├── jwt_urls.py
│   └── permissions.py
├── config/               # Конфигурация проекта
│   ├── settings.py
│   └── urls.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── .env
```
## 💻 Локальный запуск без Docker

```bash
# Активация виртуального окружения (если используется venv)
source .venv/bin/activate

# Установка зависимостей
poetry install

# Запуск сервера
python manage.py runserver
---

## 🧪 Тестирование

```bash
pytest --cov=.
```

> Покрытие тестами >90%

---

## 🔒 Безопасность и права

- Ограничения по ролям и доступу к объектам
- ALLOWED_HOSTS + .env
- Кастомные permissions на объявления
- JWT-аутентификация

---

## 📜 Лицензия

Проект открыт для использования и модификации.
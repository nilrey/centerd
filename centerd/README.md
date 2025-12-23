# CenterD - Система управления паспортами ФОИВ

Django-приложение для управления информацией об организациях (Федеральных органах исполнительной власти).

## Технологический стек

- **Python 3.7+**
- **Django 3.2.23**
- **PostgreSQL**
- **Bootstrap 5**
- **jQuery**

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd centerd
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
```

### 3. Активация виртуального окружения

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

Скопируйте файл `.env.example` в `.env` и заполните необходимые значения:

```bash
cp .env.example .env
```

Отредактируйте `.env` файл:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=eif_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
```

### 6. Создание базы данных

Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE eif_db;
```

### 7. Применение миграций

```bash
python manage.py migrate
```

### 8. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 9. Запуск сервера разработки

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

## Структура проекта

- **centerd/** - Основные настройки проекта
- **core/** - Базовые компоненты (шаблоны, статические файлы)
- **pages/** - Основные страницы сайта (главная, о нас, контакты, отзывы)
- **organizations/** - Управление организациями
- **webmail/** - Почтовый функционал (в разработке)
- **inform_objects/** - Информационные объекты (в разработке)

## Основные функции

### Управление организациями
- Список организаций
- Паспорт организации
- Структура руководства
- Правовые документы
- Информационные системы
- Контакты

### Система отзывов
- Добавление отзывов
- Просмотр всех отзывов
- Модерация отзывов

## Разработка

### Создание миграций

```bash
python manage.py makemigrations
```

### Применение миграций

```bash
python manage.py migrate
```

### Сбор статических файлов

```bash
python manage.py collectstatic
```

## Безопасность

**Важно:** Перед развертыванием в продакшене:

1. Измените `SECRET_KEY` в `.env` файле
2. Установите `DEBUG=False`
3. Настройте `ALLOWED_HOSTS` с реальными доменами
4. Используйте HTTPS
5. Настройте безопасную базу данных
 
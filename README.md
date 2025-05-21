# Сервис рассылки уведомлений

## 📌 Описание проекта

Сервис предназначен для отправки уведомлений пользователям по Email или в Telegram с возможностью отложенной отправки.  
Работает через REST API и использует Celery для асинхронной обработки.

## ⚙️ Возможности

- Отправка сообщений по email и Telegram
- Поддержка одного или нескольких получателей
- Задержка отправки: немедленно, через 1 час или через 1 день
- Логирование каждой попытки отправки в базу данных
- Асинхронная очередь задач через Celery

## 🛠 Стек технологий

- Язык: Python 3.10+
- Фреймворк: Django 4.x
- Очередь задач: Celery + Redis
- Email: SMTP-сервер
- Telegram: Telegram Bot API
- База данных: PostgreSQL

## 🚀 Установка и запуск

### 🔴1. Клонирование репозитория

```bash
git clone git@github.com:holdlemon/Sending_messages.git
cd Sending_messages
```

### 🔴2. Создание и активация виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate  # Для Windows
```

### 🔴3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 🔴4. Настройка переменных окружения

Создайте файл .env и укажите настройки для SMTP и Telegram:
```
SECRET_KEY=
DEBUG=

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=

BOT_TOKEN=
```

### 🔴5. Настройка базы данных

Перед запуском необходимо создать базу данных в PostgreSQL и обновить настройки в `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'POSTGRES_DB': 'your_db_name',
        'POSTGRES_USER': 'your_db_user',
        'POSTGRES_PASSWORD': 'your_db_password',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
    }
}
```

### 🔴6. Выполнение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 🔴7. Запуск Redis

Запустите брокер сообщений `redis-server`, если установлен локально.
Ниже вариант, если локально не установлен.
```bash
docker run -d -p 6379:6379 redis
```

### 🔴8. Запуск сервера

```bash
python manage.py runserver
```

### 🔴9. Запуск Celery

```bash
celery -A config worker --pool=solo --loglevel=info
```

Приложение доступно по адресу: [http://127.0.0.1:8000/api/notify/](http://127.0.0.1:8000/api/notify/)

## 🧪 Пример запроса к API

Сервис имеет одну точку входа:
`/api/notify/`

Тело запроса включает следующие параметры:
```
{
  "message": string(1024),
  "recepient": string(150) | list[string(150)],
  "delay": int
}
```

- Параметр `message` содержит обычный текст, который будет отправлен в сообщении

- Параметр `recepient` может содержать одного получателя или список получателей. 
При этом необходимо определять для каждого получателя, предоставлен адрес для отправки на почту или в telegram.

- Параметр `delay` отвечает за задержку отправки, где:

  `0` - отправлять без задержки, при получении запроса
  
  `1` - отправить с задержкой в 1 час
  
  `2` - отправить с задержкой в 1 день

## 📜 Лицензия

Этот проект распространяется под MIT License.

---
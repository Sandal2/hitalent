````markdown
# Решение тестового задания в hitalent

## Функции

- REST API на Django
- PostgreSQL база данных
- Docker и Docker Compose
- Автоматические миграции при старте контейнера

## Эндпоинты

- `/admin/` — панель администратора
- `/chats/` — создание чата
- `/chats/<chat_id>/messages/` — создание сообщения
- `/chats/<id>/` — детальный просмотр чата / каскадное удаление чата

## Быстрый старт

1. Клонировать репозиторий и перейти в папку:

```bash
git clone <repo-url>
cd hitalent
````

2. Создать `.env` с настройками БД и Django:

```env
DJANGO_SECRET_KEY=django_secret_key
DEBUG=true_or_false
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=db_name
DB_USER=user
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432
```

3. Запустить проект через Docker:

```bash
docker-compose up -d --build
```

4. Проверить логи (опционально):

```bash
docker-compose logs -f
```

5. Django доступен на [http://localhost:8000](http://localhost:8000)

## Основные команды

* Создать суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```

* Запуск тестов:

```bash
docker-compose exec web pytest
```

* Остановить контейнеры:

```bash
docker-compose down
```

* Пересобрать контейнеры:

```bash
docker-compose up --build
```

## Примечания

* Скрипт `wait-for-it.sh` ждёт готовность PostgreSQL перед запуском Django.

```

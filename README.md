# FoodGram

![foodgram](https://github.com/AntonLukin1986/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Сервис для публикации кулинарных рецептов

### Сервис FoodGram позволяет пользователям публиковать рецепты различных блюд, с которыми может ознакомиться любой желающий. Реализована возможность подписываться на авторов рецептов и добавлять понравившиеся блюда в «Избранное». Кроме того, пользователи имеют возможность составить «Корзину покупок». В ней будет сформирован список ингредиентов, необходимых для приготовления выбранных блюд, который можно скачать перед походом в продуктовый магазин

### Технологии

- Python
- Django
- Django Rest Framework
- PostgresQL
- Docker

### Как запустить проект

Убедитесь, что у вас установлены Docker и docker-compose.

Клонировать репозиторий:

```bash
git clone https://github.com/AntonLukin1986/foodgram-project-react
```

Перейти в директорию с файлом docker-compose.yaml:

```bash
cd infra/
```

Создать .env файл по следующему шаблону:

```text
SECRET_KEY=1a2b3c # секретный ключ джанго-проекта (установите свой)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=database
DB_PORT=5432
ALLOWED_HOSTS=localhost (добавьте необходимые хосты через пробел)
```

Выполнить команду:

```bash
sudo docker-compose up -d
```

Далее необходимо выполнить миграции, создать суперпользователя и собрать статику, выполнив по очереди следующие команды:

```bash
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

#### Заполнение базы данных ингредиентами

Ингредиенты для заполнения базы данных расположены в директории **data** контейнера **backend**.
Там же находится скрипт **csv_to_sqlite.py** для заполнения базы данных **SQLite3**.

```bash
sudo docker-compose exec backend python data/csv_to_sqlite.py
```

#### Документация к API

Документация доступна локально по ссылке: `http://localhost/api/docs/` <br>
На работающем сайте: [документация](http://51.250.24.175/api/docs/)

#### Ознакомиться с запущенным проектом можно по ссылкам

[главная страница](http://51.250.24.175/api/docs/) <br>
[админка](http://51.250.24.175/admin/) <span style="color:red">(Никнейм: admin. Пароль: admin)</span>

#### Автор проекта

***Антон Лукин*** [AntonLukin1986](https://github.com/AntonLukin1986)

#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

# Здесь нет команды makemigrations, потому что контейнер запущен не от root, а от app юзера без привилегий.
# При попытке выполнить эту команду внутри контейнера выдаст ошибку, например, такую:
# PermissionError: [Errno 13] Permission denied: '/marketplace/product/migrations/0003_alter_order.py'
# Можно выполнить команду '''docker-compose run --rm backend sh -c "python manage.py makemigrations" .'''
# (я так понимаю, она работает, поскольку стоит маппинг томов и изменения происходят не внутри контейнера,
# а на хосте [хотя странно, по-моему наоборот: изменения происходят от непривилегированного юзера внутри контейнера,
# а изменения отображаются на хосте, короче, не совсем понятно])


uwsgi --socket :9000 --workers 4 --master --enable-threads --module backend.wsgi
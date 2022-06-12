import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Кастомная команда, исполняющая перед стартом проекта - ожидает готовность БД перед подключением"""
    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Connecting to DB...')  # standard output - выводит логи на скрин
        db_up = False  # по умолчанию False
        while db_up is False:
            try:
                self.check(databases=['default'])  # метод check проверяет конфигурации Django, вернет Excepyion, если что-то не так
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
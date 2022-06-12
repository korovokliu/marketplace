""" Тесты для всех моделей """

from django.test import TestCase
from django.contrib.auth import get_user_model  # вместо абсолютного импорта лучше использовать эту функцию,
# так мы убедимся, что кастомный юзер будет дефолтным для проекта


class ModelTests(TestCase):

    def test_create_user_with_from_email(self):
        """" Ecли дефолтная модель использует username как PrimaryKey, то наша будет использовать email,
            этот код проверяет, что нам достаточно прокинуть уникальный email, чтобы создать юзера """
        email = 'test@email.com'
        password = 'user_password'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))  # т.к. пароли хранятся в зашифрованном виде, то используем
        # эту функцию, чтобы проверить хеш строки с хешем сохраненного пароля


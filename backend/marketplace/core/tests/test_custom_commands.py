"""" Тестируем свои кастомные команды """
from unittest.mock import patch  # импортируем mock, чтобы имитировать поведение БД (отправление сообщения о готовности)
from psycopg2 import OperationalError as Psycopg2Error  # импортируем потенциальную ошибку, которая возникает, когда мы пытаемся подключиться к БД, до того, как она полностью готова
from django.db.utils import OperationalError  # тоже потенциальная ошибка, но уже выбрасываемая Django
from django.core.management import call_command  # helper function от Django, которая позволяет симулировать команды
from django.test import SimpleTestCase  # в данном случае мы тестируем команду, а не БД (вместо БД у нас симуляция mock), поэтому используем SimpleTestCase, а не TestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        """ Тестирует команду ожидания БД перед полной готовностью """
        patched_check.return_value = True  # проверяем, что команда в принципе может быть вызвана
        call_command('wait_for_db')  # симулирует вызов команды из CLI
        patched_check.assert_called_once_with(database=['default'])  # после того как бд инициализируется и станет
        # доступной как default бд, эта команда вызовется последний раз - подтвердит доступность и уйдет на покой

    @patch('time.sleep')  # имитируем ожидание, перед тем как снова вызвать wait_for_db
    def test_wait_for_db_delay(self, patched_sleep, patched_check):  # порядок аргументов важен, сначала mock декоратора на эту функцию, потом на весь класс
        patched_check.side_effect = [Psycopg2Error]*2 + [OperationalError]*3 + [True]
        # В библиотеке Python unittest.mock side_effect — это атрибут, который позволяет управлять поведением
        # фиктивного объекта. Он позволяет указать список возвращаемых значений, которые фиктивный объект должен
        # возвращать при каждом вызове.
        # В этом конкретном примере patched_check имитируется, чтобы вызывать определенные исключения
        # при многократном вызове.
        # side_effect атрибут является списком. И список этот состоит из двух ошибок Psycopg2Error после первых двух
        # вызовов patched_check, трех ошибок OperationalError после следующих трех вызовов patched_check и в конечном
        # счёте True на последнем вызове patched_check (БД готова и принимает подключения)
        # 2 и 3 на самом деле выбраны произвольно, но примерно столько раз могут выкидываться эти ошибки, если
        # поставить 10 и 20, ничего не поменяется
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(database=['default'])


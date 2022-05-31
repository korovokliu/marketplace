from django.db import models
from product.models import Product


class Credentials(models.Model):
    class PaymentType(models.TextChoices):
        CARD = ('Онлайн оплата', 'Онлайн оплата')
        CASH = ('Наличные курьеру', 'Наличные курьеру')
    first_name = models.CharField(verbose_name="Имя", max_length=50)
    last_name = models.CharField(verbose_name="Фамилия", max_length=50)
    email = models.EmailField()
    address = models.CharField(verbose_name="Адрес", max_length=250)
    city = models.CharField(verbose_name="Город", max_length=100)
    created = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    payment_type = models.CharField(verbose_name="Тип оплаты", max_length=32,
                                    choices=PaymentType.choices, default=PaymentType.CARD)


    class Meta:
            ordering = ['-created']
            indexes = [
                models.Index(fields=['-created']),
            ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
#    delivery_info = models.ForeignKey(Credentials, verbose_name="Данные заказа", related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.product.discount_price * self.quantity

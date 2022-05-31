from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    name = models.CharField(verbose_name="Имя категории", max_length=255, unique=True)
    slug = models.SlugField(verbose_name="Ссылка", max_length=255, unique=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def get_absolute_url(self):
        return reverse("products:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(verbose_name="Название товара", max_length=200)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.RESTRICT)
    regular_price = models.DecimalField(verbose_name="Цена без скидки", decimal_places=2, max_digits=14)
    discount_price = models.DecimalField(verbose_name="Цена co скидкой", decimal_places=2, max_digits=14)
    image = models.ImageField(verbose_name="Фото товара", upload_to=f'product/')
    slug = models.SlugField(verbose_name="Уникальная ссылка", max_length=250, unique=True)
    in_sale = models.BooleanField(verbose_name="В продаже?", default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:individual_product', args=[self.slug])

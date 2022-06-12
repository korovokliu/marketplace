from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """ Иерархические категории товаров """
    slug = models.SlugField(verbose_name="Ссылка", max_length=255, unique=True, primary_key=True)
    name = models.CharField(verbose_name="Имя категории", max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    # properties = models.ManyToManyField(Properties, through='CategoryProperty', related_name="categories")

    class MPTTMeta:
        order_insertion_by = ["name"]

    def get_absolute_url(self):
        return reverse("products:category_list", args=[self.slug])

    def __str__(self):
        return self.name

class Properties(models.Model):
    """ Здесь хранятся все возможные свойства для разных категорий товаров: CPU, RAM, графический процессор для
    ноутбуков; размер, длина, тип ткани для одежды и т.п."""
    property_name = models.CharField(primary_key=True, null=False, unique=True, blank=False, max_length=200, verbose_name="Название характеристики товара")
    categories = models.ManyToManyField(Category, through='CategoryProperty', through_fields=('property_name', 'category'), related_name="properties")
    def __str__(self):
        return self.property_name

class Product(models.Model):
    """ Конкретный товар на маркетплейсе """
    title = models.CharField(verbose_name="Название товара", max_length=200)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.RESTRICT, related_name="products_in_that_category", to_field='name')
    regular_price = models.DecimalField(verbose_name="Цена без скидки", decimal_places=2, max_digits=14)
    discount_price = models.DecimalField(verbose_name="Цена co скидкой", decimal_places=2, max_digits=14)
    image = models.ImageField(verbose_name="Фото товара", upload_to=f'product/', null=True, blank=True)
    slug = models.SlugField(verbose_name="Уникальная ссылка", max_length=250, unique=True)
    in_sale = models.BooleanField(verbose_name="В продаже?", default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:individual_product', args=[self.slug])


class CategoryProperty(models.Model):
    """ Таблица для связи Many-To-Many - многим категориям могут соответствовать разные спецификации (например,
    'цвет' могут использовать ноутбуки и одежда """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_to_properties", to_field='name')
    property_name = models.ForeignKey(Properties, on_delete=models.CASCADE, related_name="category_to_property", to_field='property_name')


class PropertyValues(models.Model):
    """ Конкретные значения для характеристик, например Intel i9-12900HK для CPU, red для color и т.п. """
    name = models.CharField(max_length=255, unique=True)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE, related_name="related_to_value", to_field='property_name')

    def __str__(self):
        return self.name


class ProductToPropertyValues(models.Model):
    """ Промежуточная таблица для Many-To-Many связи между Product и PropertyValue (одному товару
    могут соответствовать много значений доп. свойств, и каждое значение доп. свойства может
    принадлежать многим товарам """

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="additional_property_values")
    property_values_id = models.ForeignKey(PropertyValues, on_delete=models.RESTRICT, related_name="related_to_products", to_field='name')

    def __str__(self):
        return f"Product {self.product_id.name} have property {self.property_values_id.name}"


class ClothesSizePropertyValues(models.Model):
    """ Для размеров одежды отдельный класс, потому что значений характеристики Size может быть несколько
    для одного товара """
    class Sizes(models.TextChoices):
        xxs = ('XXS', 'XXS')
        xs = ('XS', 'XS')
        s = ('S', 'S')
        m = ('M', 'M')
        l = ('L', 'L')
        xl = ('XL', 'XL')
        xxl = ('XXL', 'XXL')
        three_xl = ('3XL', '3XL')
        without = ('Any size', 'Универсальный размер')

    letter_code = models.CharField(choices=Sizes.choices, max_length=10, verbose_name="Буквенный код")
    europe_num_size = models.IntegerField(verbose_name="Европейский размер")
    UK_num_size = models.IntegerField(verbose_name="Британский размер")
    USA_num_size = models.IntegerField(verbose_name="Размер США")

    def __str__(self):
        return self.letter_code


class ClothesSizePropertyValuesToProduct(models.Model):
    """ Таблица для Many-To-Many связи: конкретному товару с одеждой на маркетплейсе
    могут соответствовать несколько размеров, так же как и один размер может соответствовать
    нескольким товарам
    """
    clothes_id = models.ForeignKey(ClothesSizePropertyValues, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

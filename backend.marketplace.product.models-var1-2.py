from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
class Colors(models.Model):
    name = models.CharField(primary_key=True, max_length=150)


class Sizes(models.Model):
    size = models.CharField(primary_key=True, max_length=8)


class Fabric(models.Model):
    fabric = models.CharField(primary_key=True, max_length=250)


class ClothesSpecification(models.Model):
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

    size = models.CharField(choices=Sizes.choices, max_length=10, verbose_name="Размер")
    color = models.ForeignKey(Colors, on_delete=models.RESTRICT, verbose_name="Цвет")
    fabric_name = models.ForeignKey(Fabric, on_delete=models.RESTRICT, verbose_name="Тип ткани")

class TopClothesSpecification(models.Model):
    class NeckLineType(models.TextChoices):
        u_shape = ('U-shape', 'U-образный')
        v_shape = ('V-shape', 'V-образный')
        round = ('Round', 'Круглый')
        plunging = ('Plunging', 'Глубокий')
        collar = ('Collar', 'Воротник')
        halter = ('Halter', 'Халтер')
        turtleneck = ('Turtleneck', 'Водолазка')
        other = ('Other', 'Другое')

    class SleevesLength(models.TextChoices):
        without = ('No sleeves', 'Без рукавов')
        short = ('Short', 'Короткий')
        elbow = ('Above elbow', 'До локтя')
        long = ('Long', 'Длинный')


    neckline_type = models.CharField(choices=NeckLineType.choices, max_length=10, verbose_name="Тип выреза")
    sleeves_type = models.CharField(choices=SleevesLength.choices, max_length=11, verbose_name="Длина рукава")
    clothes_characteristics = models.ForeignKey(ClothesSpecification, on_delete=models.CASCADE)


class Category(MPTTModel):
    slug = models.SlugField(verbose_name="Ссылка", max_length=255, unique=True, primary_key=True)
    name = models.CharField(verbose_name="Имя категории", max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    specifications = models.ManyToManyField(Specification, related_name='categories')

    def parent_and_ancestor_specifications(self):
        specifications = self.specifications.all()
        if self.parent:
            parent_specifications = self.parent_and_ancestor_specifications()
            specifications = specifications | parent_specifications
        return specifications

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
    image = models.ImageField(verbose_name="Фото товара", upload_to=f'product/', null=True, blank=True)
    slug = models.SlugField(verbose_name="Уникальная ссылка", max_length=250, unique=True)
    in_sale = models.BooleanField(verbose_name="В продаже?", default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:individual_product', args=[self.slug])


# class Specification(models.Model):
#     category_id = models.ForeignKey()
#     name = models.CharField()


class ProductSpecificationValue(models.Model):
    """
    The Product Specification Value table holds each of the
    products individual specification or bespoke features.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(verbose_name="Значение", max_length=255)

    def __str__(self):
        return self.value


class ProductSpecification(models.Model):
    """
    The Product Specification Table contains product
    specifiction or features for the product types.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    def __str__(self):
        return self.name
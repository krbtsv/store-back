import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True, verbose_name='Картинка')
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name='Категория')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None,
                                  update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='rub'
        )
        return stripe_product_price

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category}'

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def create_stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def sum(self):
        return self.quantity * self.product.price

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id, user):
        basket = Basket.objects.filter(user=user, product_id=product_id)

        if not basket.exists():
            obj = Basket.objects.create(user=user, product_id=product_id, quantity=1)
            is_created = True
            return obj, is_created
        else:
            basket = basket.first()
            basket.quantity += 1
            basket.save()
            is_created = False
            return basket, is_created

    class Meta:
        db_table = 'basket'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['id']

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

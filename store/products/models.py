from django.db import models


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
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Картинка')
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category}'

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['id']


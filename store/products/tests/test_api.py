from rest_framework import status
from rest_framework.test import APITestCase
from products.models import ProductCategory, Product
from products.serializers import ProductCategorySerializer, ProductSerializer


class ProductsAPITestCase(APITestCase):
    def setUp(self):
        ProductCategory.objects.create(name='Одежда')
        ProductCategory.objects.create(name='Обувь')
        ProductCategory.objects.create(name='Аксессуры')

        Product.objects.create(name='Ботинок', description='Прочный', price=100, quantity=5, category_id=2)
        Product.objects.create(name='Пальто', description='Шикарное', price=150, quantity=7, category_id=1)
        Product.objects.create(name='Сумка', description='Слезы крокодила', price=200, quantity=15, category_id=3)

    def test_get_product_category(self):
        url = 'http://127.0.0.1:8000/store_dress_api/categories/'
        response = self.client.get(url)
        categories = ProductCategory.objects.all()

        serializer_data = ProductCategorySerializer(categories, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_products(self):
        url = 'http://127.0.0.1:8000/store_dress_api/products/'
        response = self.client.get(url)
        products = Product.objects.all()

        serializer_data = ProductSerializer(products, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

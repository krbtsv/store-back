from rest_framework import status
from rest_framework.test import APITestCase
from products.models import ProductCategory
from products.serializers import ProductCategorySerializer


class ProductCategoryAPITestCase(APITestCase):
    def setUp(self):
        ProductCategory.objects.create(name='Одежда')
        ProductCategory.objects.create(name='Обувь')
        ProductCategory.objects.create(name='Аксессуры')

    def test_get_product_category(self):
        url = 'http://127.0.0.1:8000/store_dress_api/categories/'
        response = self.client.get(url)
        categories = ProductCategory.objects.all()

        serializer_data = ProductCategorySerializer(categories, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

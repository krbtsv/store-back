from django.urls import path

from store_dress_api.views import ProductListAPIView

app_name = 'store_dress_api'

urlpatterns = [
    path('product-list/', ProductListAPIView.as_view(), name='product_list'),
]

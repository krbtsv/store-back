from django.urls import include, path
from rest_framework import routers

from store_dress_api.views import BasketModelViewSet, ProductModelViewSet, ProductCategoryModelViewSet

app_name = 'store_dress_api'

router = routers.DefaultRouter()
router.register(r'categories', ProductCategoryModelViewSet)
router.register(r'products', ProductModelViewSet)
router.register(r'baskets', BasketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

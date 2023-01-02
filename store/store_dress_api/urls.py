from django.urls import include, path
from rest_framework import routers

from store_dress_api.views import ProductModelViewSet

app_name = 'store_dress_api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

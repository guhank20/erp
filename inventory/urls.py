from django.urls import path, include
from .views import WarehouseListCreateView, InventoryViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'inverntory', InventoryViewSet, basename='inventory')


urlpatterns = [
    path('warehouses/', WarehouseListCreateView.as_view(), name='Warehouse-list-create'),
    path('', include(router.urls)),
]




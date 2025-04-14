from django.urls import path, include
from .views import WarehouseListCreateView, InventoryViewSet, transaction_item_list_view
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'inverntory', InventoryViewSet, basename='inventory')


urlpatterns = [
    path('warehouses/', WarehouseListCreateView.as_view(), name='Warehouse-list-create'),
    path('', include(router.urls)),
    path('transaction-items/', transaction_item_list_view, name='transaction-item-list'),
]




from .models import Warehouse, Inventory, TransactionItem
from django.core.exceptions import ValidationError
from .serializers import TransactionItemSerializer
from django.contrib.contenttypes.models import ContentType
from rest_framework.pagination import PageNumberPagination
import logging
from rest_framework.response import Response
from rest_framework import status

# Create a logger
logger = logging.getLogger(__name__)

def create_warehouse(data):
    return Warehouse.objects.create(**data)

def get_all_warehouses():
    return Warehouse.objects.all()

def get_warehouse_by_id(warehouse_id):
    return Warehouse.objects.get(id=warehouse_id)


def validate_inventory_data(data):
    product_name = data.get('product_name')
    # Example: Ensure quantity is not negative
    if data.get('quantity', 0) < 0:
        raise ValidationError("Quantity cannot be negative.")

    # Example: Product name should be unique (if not using serializer to enforce)
    if product_name and Inventory.objects.filter(product_name=data['product_name']).exists():
        raise ValidationError("Product name must be unique.")

    return data


def create_inventory(data):
    validate_inventory_data(data)
    return Inventory.objects.create(**data)


def update_inventory(instance, data):
    product_name = data.get('product_name')
    if product_name and product_name != instance.product_name:
        if Inventory.objects.filter(product_name=product_name).exclude(id=instance.id).exists():
            raise ValidationError("Product name must be unique.")
    
    validate_inventory_data(data)
    
    for attr, value in data.items():
        setattr(instance, attr, value)
    instance.save()
    return instance

def delete_inventory(instance):
    instance.delete()

def transaction_items(request):
    product_id = request.GET.get('product_id')
    filter_type = request.GET.get('filter_type')  # e.g., 'sale', 'purchase'

    queryset = TransactionItem.objects.all()

    if product_id:
        queryset = queryset.filter(product_id=product_id)

    if filter_type:
        content_type = ContentType.objects.get(model=filter_type)
        queryset = queryset.filter(content_type=content_type)

    page_size = request.GET.get('page_size', 10)  # Default to 10 if not specified
    try:
        page_size = int(page_size)  # Ensure it's an integer
    except ValueError:
        page_size = 10
    queryset = queryset.order_by('id')
    logger.error(f"Invalid content type: {filter_type}")
    logger.error(f"Invalid query: {queryset}")
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(queryset, request)

    serializer = TransactionItemSerializer(result_page, many=True)
    result =  paginator.get_paginated_response(serializer.data)
    return result.data

def create_transaction_item(data,content_type,ref_id):
    return TransactionItem.create_transaction_items(data,content_type,ref_id)

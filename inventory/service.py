from .models import Warehouse, Inventory
from django.core.exceptions import ValidationError

def create_warehouse(data):
    return Warehouse.objects.create(**data)

def get_all_warehouses():
    return Warehouse.objects.all()

def get_warehouse_by_id(warehouse_id):
    return Warehouse.objects.get(id=warehouse_id)


def validate_inventory_data(data):
    # Example: Ensure quantity is not negative
    if data.get('quantity', 0) < 0:
        raise ValidationError("Quantity cannot be negative.")

    # Example: Product name should be unique (if not using serializer to enforce)
    if Inventory.objects.filter(product_name=data['product_name']).exists():
        raise ValidationError("Product name must be unique.")

    return data


def create_inventory(data):
    validate_inventory_data(data)
    return Inventory.objects.create(**data)


def update_inventory(instance, data):
    if 'product_name' in data and data['product_name'] != instance.product_name:
        if Inventory.objects.filter(product_name=data['product_name']).exclude(id=instance.id).exists():
            raise ValidationError("Product name must be unique.")
    
    validate_inventory_data(data)
    
    for attr, value in data.items():
        setattr(instance, attr, value)
    instance.save()
    return instance

def delete_inventory(instance):
    instance.delete()
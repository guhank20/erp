from inventory.models import TransactionItem
from sales.models import Sales
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

def create_sales(data):
    items_data = data.pop('item_inputs', [])
    sale = Sales.objects.create(**data)
    content_type = ContentType.objects.get_for_model(Sales)

    for item in items_data:
        try:
            TransactionItem.objects.create(
                content_type=content_type,
                object_id=sale.id,
                **item
            )
        except ValidationError as e:
            logger.error(f"Validation error for item {item}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for item {item}: {e}")
    return sale

def update_sales(instance, data):
    items_data = data.pop('item_inputs', None)

    for attr, value in data.items():
        setattr(instance, attr, value)
    instance.save()

    if items_data is not None:
        TransactionItem.objects.filter(
            content_type=ContentType.objects.get_for_model(Sales),
            object_id=instance.id
        ).delete()
        for item in items_data:
            TransactionItem.objects.create(
                content_type=ContentType.objects.get_for_model(Sales),
                object_id=instance.id,
                **item
            )
    return instance
def delete_sales(instance):
    TransactionItem.objects.filter(
        content_type=ContentType.objects.get_for_model(Sales),
        object_id=instance.id
    ).delete()
    instance.delete()

def list_sales_by_id(sale_id):
    try:
        sale = Sales.objects.get(id=sale_id)
    except Sales.DoesNotExist:
        return None

    content_type = ContentType.objects.get_for_model(Sales)
    sale.items = TransactionItem.objects.filter(
        content_type=content_type,
        object_id=sale.id
    )
    return sale
from inventory.models import TransactionItem
from purchase.models import Purchase
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

def create_purchase(data):
    items_data = data.pop('item_inputs', [])
    purchase = Purchase.objects.create(**data)
    content_type = ContentType.objects.get_for_model(Purchase)

    for item in items_data:
        try:
            TransactionItem.objects.create(
                content_type=content_type,
                object_id=purchase.id,
                **item
            )
        except ValidationError as e:
            logger.error(f"Validation error for item {item}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for item {item}: {e}")
    return purchase

def update_purchase(instance, data):
    items_data = data.pop('item_inputs', None)

    for attr, value in data.items():
        setattr(instance, attr, value)
    instance.save()

    if items_data is not None:
        TransactionItem.objects.filter(
            content_type=ContentType.objects.get_for_model(Purchase),
            object_id=instance.id
        ).delete()
        for item in items_data:
            TransactionItem.objects.create(
                content_type=ContentType.objects.get_for_model(Purchase),
                object_id=instance.id,
                **item
            )
    return instance
def delete_purchase(instance):
    TransactionItem.objects.filter(
        content_type=ContentType.objects.get_for_model(Purchase),
        object_id=instance.id
    ).delete()
    instance.delete()

def list_purchase_by_id(purchase_id):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
    except Purchase.DoesNotExist:
        return None

    content_type = ContentType.objects.get_for_model(Purchase)
    purchase.items = TransactionItem.objects.filter(
        content_type=content_type,
        object_id=purchase.id
    )
    return purchase
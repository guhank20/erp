from django.db import models
from users.models import BaseModel
from inventory.models import TransactionItem
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class Purchase(BaseModel):
    supplier_name = models.CharField(max_length=200, blank=False)
    status = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'purchase'
    def get_items(self):
        return TransactionItem.objects.filter(
            content_type=ContentType.objects.get_for_model(Purchase),
            object_id=self.id
        )
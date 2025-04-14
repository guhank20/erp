from django.db import models
from users.models import BaseModel, CustomUser
from inventory.models import TransactionItem
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class Sales(BaseModel):
    customer_name = models.CharField(max_length=200, blank=False)
    status = models.BooleanField(default=False)
    order_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True)
    class Meta:
        db_table = 'sales'

    def get_items(self):
        return TransactionItem.objects.filter(
            content_type=ContentType.objects.get_for_model(Sales),
            object_id=self.id
        )
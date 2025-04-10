from django.db import models
from users.models import BaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal

# Create your models here.

class Warehouse(BaseModel):
    name = models.CharField(max_length=50, blank=False, unique=True)
    location = models.CharField(max_length=200, blank=False)
    capacity = models.DecimalField(max_digits=50, decimal_places=2)
    class Meta:
        db_table = 'warehouse'

class Inventory(BaseModel):
    product_name = models.CharField(max_length=200 , blank=False, unique=True)
    category = models.IntegerField(max_length=10, blank=False)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    supplier_id = models.IntegerField(max_length=5, null=True, blank=True)
    price = models.IntegerField(blank=False, default=0)
    available_qty = models.IntegerField(blank=False, default=0)
    threshold = models.IntegerField(blank=False, default=0)
    class Meta:
        db_table = 'inventory'

class TransactionItem(models.Model):
    # Polymorphic link
    content_type = models.ForeignKey(ContentType,null=True, blank=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField()
    parent = GenericForeignKey('content_type', 'object_id')

    # Related data
    product = models.ForeignKey(Inventory,null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField()
    per_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        # Auto-calculate total price
        if self.quantity and self.per_price is not None:
            self.price = Decimal(self.quantity) * self.per_price
        super().save(*args, **kwargs)




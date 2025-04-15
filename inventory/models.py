from django.db import models
from users.models import BaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models import Sum
from purchase.models import Purchase
from sales.models import Sales
import threading

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
    active = models.BooleanField(default=True)
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

    @classmethod
    def create_transaction_items(cls, data, content_type_model, ref_id):
        content_type = ContentType.objects.get_for_model(content_type_model)
        success = False
        for item in data:
            if item['product_id']:
                try:
                    isCreate = False
                    if content_type_model == Sales:
                        thread_sales = threading.Thread(target=cls.get_product_credit, args=(item['product_id'],Sales,))
                        thread_purchase = threading.Thread(target=cls.get_product_credit, args=(item['product_id'],Purchase,))
                        thread_sales.start()
                        thread_purchase.start()

                        thread_sales.join()
                        thread_purchase.join()
                    else:
                        isCreate = True
                    if isCreate:
                        cls.objects.create(
                            content_type=content_type,
                            object_id=ref_id,
                            **item
                        )
                        success = True
                except ValidationError as e:
                    success = False
                except Exception as e:
                    success = False
        return success
    
    @classmethod
    def get_product_credit(cls,product_id,content_type_model):
        if content_type_model is None:
            content_type_model = Purchase
        
        result = cls.objects.filter(
            product_id=product_id,
            content_type=content_type_model
        ).aggregate(total_qty=Sum('quantity'))

        return result['total_qty'] or 0
    
    @classmethod
    def get_product_debit(cls,product_id,content_type_model):
        if content_type_model is None:
            content_type_model = Sales
        
        result = cls.objects.filter(
            product_id=product_id,
            content_type=content_type_model
        ).aggregate(total_qty=Sum('quantity'))

        return result['total_qty'] or 0
    








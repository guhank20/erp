from django.db import models
from users.models import BaseModel

# Create your models here.


class Purchase(BaseModel):
    supplier_name = models.CharField(max_length=200, blank=False)
    status = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'purchase'
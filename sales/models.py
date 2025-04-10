from django.db import models
from users.models import BaseModel, CustomUser

# Create your models here.


class Sales(BaseModel):
    customer_name = models.CharField(max_length=200, blank=False)
    status = models.BooleanField(default=False)
    order_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True)
    class Meta:
        db_table = 'sales'
from django.db import models
from django.conf import settings

# Create your models here.
class Order(models.Model):

    username= models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    email = models.CharField(max_length=250 , null=True)
    session= models.CharField(max_length=250, null=True)
    code_mail = models.CharField(max_length=250, null=True)
    zarinpal_authority = models.CharField(max_length=255 , blank=True)
    ref_id = models.CharField(max_length=155 , blank=True)
    zarinpal_data=models.TextField(blank=True)
    is_paid = models.BooleanField(default=False , null=True)

    orders_note = models.TextField(blank=True )

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.username 
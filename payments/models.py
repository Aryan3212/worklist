from django.db import models
from django.conf import settings
import uuid

# status = models.CharField(choices=PAYMENT_STATUS, default='PENDING')
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.DO_NOTHING,
    # )
    # currency = models.CharField(max_length=3, default='BDT')
    # shipping_method = models.CharField(max_length=2, default='NO')
    # amount = models.DecimalField(default=500.00, max_digits=5, decimal_places=2)
    # emi_option = models.IntegerField(default=0)
    # product_name = models.CharField(max_length=200, default='WorkList Job Listing')
    # product_category = models.CharField(max_length=200, default='general')
    # product_profile = models.CharField(max_length=200, default='non-physical-goods')
    # cus_email = models.EmailField()
    # cus_name = models.CharField(max_length=200, null=True, default='')
    # cus_add1 = models.CharField(max_length=200, null=True, default='')
    # cus_city = models.CharField(max_length=200, null=True, default='')
    # cus_country = models.CharField(max_length=200, null=True, default='')
    # cus_phone = models.CharField(max_length=200, null=True, default='0')
    # # TODO: only for frontend
    # sessionkey = models.CharField(max_length=200, null=True, default='')

PAYMENT_STATUS = [
    ('COMPLETED', 'COMPLETED'),
    ('PENDING', 'PENDING'),
    ('FAILED', 'FAILED'),
]


ORDER_TYPES = [
    ('JOB_POSTING', 'JOB_POSTING'),
]

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(choices=ORDER_TYPES)
    currency = models.CharField(max_length=3, default='BDT')
    amount = models.CharField()
    status = models.CharField(choices=PAYMENT_STATUS, default='PENDING')
    product_reference_id = models.UUIDField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)


LEDGER_ENTRY_TYPES = [
    ('DEBIT', 'DEBIT'),
    ('CREDIT', 'CREDIT')
]
class Ledger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(choices=LEDGER_ENTRY_TYPES)
    currency = models.CharField(max_length=3, default='BDT')
    amount = models.TextField()
    notes = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)

class PaymentArchive(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.JSONField()
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    def __str__(self) -> str:
        return self.id
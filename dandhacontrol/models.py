from django.db import models
from django.utils import timezone
import uuid
# Create your models here.

class Service(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'service'
        indexes = [
            models.Index(fields=['name'])
        ]

class PaymentMode(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_mode'


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_auth_id = models.CharField(max_length=255, null=True)
    client_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'client'
        indexes = [
            models.Index(fields=['client_auth_id']),
            models.Index(fields=['client_name'])
        ]



class Company(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255,null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    company_service = models.ManyToManyField(Service, through='CompanyServiceRelationship')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'company'
        indexes = [
            models.Index(fields=['company_name'])
        ]

class CompanyServiceRelationship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_info = models.ForeignKey(Service, on_delete=models.CASCADE)
    company_info = models.ForeignKey(Company, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company_service_relationship'

class Locality(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    area = models.CharField(max_length=255, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'locality'
        indexes = [
            models.Index(fields=['area'])
        ]
    

class Customer(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=255,null=True)
    text_address = models.JSONField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'customer'
        indexes = [
            models.Index(fields=['customer_name'])
        ]


class Package(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255,null=True)
    price_monthly = models.IntegerField()
    company_service_info = models.ForeignKey(CompanyServiceRelationship, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'package'
        indexes = [
            models.Index(fields=['name'])
        ]

class Device(models.Model):
    
    ACTIVE = 1
    NOT_ACTIVE = 0

    STATUS = (
        (ACTIVE, 'Active'),
        (NOT_ACTIVE, 'Not_Active')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_number = models.CharField(max_length=255,null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    add_on_price = models.IntegerField(default=0)
    status= models.PositiveSmallIntegerField(choices=STATUS)
    recharge_date = models.DateField()
    balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'device'

class Recharge(models.Model):
    
    YES = 1
    NO = 0

    STATUS = (
        (YES, 'Yes'),
        (NO, 'No')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    payment_collected = models.PositiveSmallIntegerField(choices=STATUS)
    payment_amount = models.IntegerField(blank=True, null=True)
    payment_date = models.DateField()
    recharge_entry = models.DateField(default=timezone.now)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recharge'

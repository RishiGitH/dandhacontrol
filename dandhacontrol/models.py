import uuid
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Count, Sum
from django.utils.functional import cached_property
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

    @cached_property
    def package_count(self):
        return self.company_service.annotate\
            (package_count=Count('packages')).\
            aggregate(total=Sum('package_count'))['total'] or 0
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

    @cached_property
    def device_count(self):
        return self.device_set.aggregate(count=Count('id'))['count']

    @cached_property
    def customer_count(self):
        return self.customer_set.aggregate(count=Count('id'))['count']

class Customer(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=255,null=True)
    text_address = models.JSONField()
    phone_number = PhoneNumberField(blank=True)
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
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    frequency = models.SmallIntegerField()
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
    add_on_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    add_on_desc = models.CharField(max_length=255, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS)
    expiry_date = models.DateField()
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'device'

class Recharge(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    recharge_entry = models.DateField(default=timezone.now)
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recharge'


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    payment_amount = models.IntegerField(blank=True, null=True)
    payment_date = models.DateField()
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment'
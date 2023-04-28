import django_filters
from .models import Package, Device, Recharge, Customer, Payment
from django.db.models import Q, F
from datetime import timedelta
from django.utils import timezone


class CustomerFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_query')
    locality = django_filters.UUIDFilter(field_name='locality__id')

    class Meta:
        model = Customer
        fields = ['query', 'locality']

    def filter_query(self, queryset, name, value):
        return queryset.filter(
            Q(customer_name__icontains=value) |
            Q(text_address__contains={'zip': value}) |
            Q(text_address__contains={'city': value}) |
            Q(text_address__contains={'street': value}) |
            Q(text_address__contains={'state': value}) |
            Q(device__device_number__icontains=value)
        ).distinct()

class PackageFilter(django_filters.FilterSet):
    company_id = django_filters.UUIDFilter(field_name="company_service_info__company_info__id")
    service_id = django_filters.UUIDFilter(field_name="company_service_info__service_info__id")

    class Meta:
        model = Package
        fields = ['company_id', 'service_id']


class DeviceFilter(django_filters.FilterSet):
    package_id = django_filters.UUIDFilter(field_name="package__id")
    locality_id = django_filters.UUIDFilter(field_name="locality__id")
    customer_id = django_filters.UUIDFilter(field_name="customer__id")
    expiry_date = django_filters.DateFilter(field_name="expiry_date")

    class Meta:
        model = Device
        fields = ['expiry_date', 'customer_id', 'locality_id', 'package_id']

class RechargeFilter(django_filters.FilterSet):
    locality_id = django_filters.UUIDFilter(field_name="device__locality__id")

    class Meta:
        model = Recharge
        fields = ['locality_id']

class PaymentFilter(django_filters.FilterSet):
    locality_id = django_filters.UUIDFilter(field_name="device__locality__id")

    class Meta:
        model = Payment
        fields = ['locality_id']

def date_range_filter(field_name, days):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    return Q(**{f"{field_name}__range": (start_date, end_date)})

def today_filter(field_name):
    return date_range_filter(field_name, 1)

def yesterday_filter(field_name):
    return date_range_filter(field_name, 2) & ~date_range_filter(field_name, 1)

def last_7_days_filter(field_name):
    return date_range_filter(field_name, 7)

def last_30_days_filter(field_name):
    return date_range_filter(field_name, 30)

def last_90_days_filter(field_name):
    return date_range_filter(field_name, 90)


class PaymentDateFilter(django_filters.FilterSet):
    date_range = django_filters.DateFromToRangeFilter(field_name='payment_date')
    client_id = django_filters.NumberFilter(field_name='customer__client_id')

    class Meta:
        model = Payment
        fields = ['date_range', 'client_id']

import django_filters
from .models import Package, Device, Recharge
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
    locality_id = django_filters.UUIDFilter(field_name="locality__id")

    class Meta:
        model = Recharge
        fields = ['locality_id']
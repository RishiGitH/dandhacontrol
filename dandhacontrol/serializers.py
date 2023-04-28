from rest_framework import serializers
from .models import Company, CompanyServiceRelationship,\
    Service,Locality,Customer,\
    Package,Device,Recharge,PaymentMode,Client, Payment
from .filters import date_range_filter,yesterday_filter\
    ,today_filter,last_7_days_filter,\
    last_30_days_filter,last_90_days_filter
from django.db.models import Count, Sum


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class BasicCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyServiceRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyServiceRelationship
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    company_service = ServiceSerializer(many=True, read_only=True)
    package_count = serializers.ReadOnlyField()

    class Meta:
        model = Company
        fields = '__all__'

    def get_field_names(self, declared_fields, info):
        field_names = super().get_field_names(declared_fields, info)
        field_names.extend(['package_count'])
        return field_names

    # def create(self, validated_data):
    #     service_ids = validated_data.pop('company_service')
    #     company_instance = Company.objects.create(**validated_data)
    #
    #     for service_id in service_ids:
    #         Service.objects.get
    #         relationship_instance = CompanyServiceRelationship(
    #             service_info=service_id,
    #             company_info=company_instance,
    #         )
    #         relationship_instance.save()
    #
    #     return company_instance


class CompanyServiceRelationshipListSerializer(serializers.ModelSerializer):
    company_info = BasicCompanySerializer(read_only=True)
    service_info = ServiceSerializer(read_only=True)
    class Meta:
        model = CompanyServiceRelationship
        fields = '__all__'

class CompanyServiceRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyServiceRelationship
        fields = '__all__'


class LocalitySerializer(serializers.ModelSerializer):
    device_count = serializers.ReadOnlyField()
    customer_count = serializers.ReadOnlyField()
    class Meta:
        model = Locality
        fields = '__all__'
    def get_field_names(self, declared_fields, info):
        field_names = super().get_field_names(declared_fields, info)
        field_names.extend(['device_count', 'customer_count'])
        return field_names

class PackageSerializer(serializers.ModelSerializer):
    company_id = serializers.CharField(write_only=True)
    service_id = serializers.CharField(write_only=True)

    class Meta:
        model = Package
        fields = ('id', 'name', 'price', 'frequency', 'company_id', 'service_id', 'created_at', 'updated_at')

    def create(self, validated_data):
        company_id = validated_data.pop('company_id')
        service_id = validated_data.pop('service_id')

        company = Company.objects.get(id=company_id)
        service = Service.objects.get(id=service_id)

        company_service_info = CompanyServiceRelationship.\
            objects.filter(company_info=company, service_info=service).first()
        package = Package.objects.create(company_service_info=company_service_info, **validated_data)
        return package

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class DeviceCustomerSerializer(serializers.ModelSerializer):
    company_service_info = CompanyServiceRelationshipSerializer(many=True, read_only=True)
    service = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ('id', 'device_number', 'package', 'locality', 'customer',
                  'add_on_price', 'add_on_desc', 'status', 'expiry_date',
                  'balance', 'created_at', 'updated_at', 'service', 'company_service_info')

    def get_service(self, obj):
        return ServiceSerializer(obj.package.company_service_info.service_info).data

class CustomerListSerializer(serializers.ModelSerializer):
    locality = LocalitySerializer(read_only=True)
    next_recharge_date = serializers.ReadOnlyField()
    devices = DeviceCustomerSerializer(many=True, read_only=True, source='device_set')

    class Meta:
        model = Customer
        fields = '__all__'

    def get_field_names(self, declared_fields, info):
        field_names = super().get_field_names(declared_fields, info)
        field_names.extend(['next_recharge_date'])
        field_names.extend(['devices'])
        return field_names


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class CompanyServiceRelationshipALLSerializer(serializers.ModelSerializer):
    company_info = BasicCompanySerializer(read_only=True)
    service_info = ServiceSerializer(read_only=True)
    class Meta:
        model = CompanyServiceRelationship
        fields = '__all__'

class PackageListSerializer(serializers.ModelSerializer):
    company_service_info = CompanyServiceRelationshipALLSerializer(read_only=True)

    class Meta:
        model = Package
        fields = ('id', 'name', 'price', 'frequency', 'company_service_info', 'created_at', 'updated_at')

class PackageALLSerializer(serializers.ModelSerializer):
    company_service_info = CompanyServiceRelationshipALLSerializer(read_only=True)
    class Meta:
        model = Package
        fields = '__all__'




class DeviceCustomSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    package = PackageALLSerializer(read_only=True)
    locality = LocalitySerializer(read_only=True)

    class Meta:
        model = Device
        fields = '__all__'

class RechargeListSerializer(serializers.ModelSerializer):
    device = DeviceCustomSerializer(read_only=True)
    class Meta:
        model = Recharge
        fields = '__all__'



class RechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recharge
        fields = '__all__'


class PaymentListSerializer(serializers.ModelSerializer):
    device = DeviceCustomSerializer(read_only=True)
    class Meta:
        model = Recharge
        fields = '__all__'



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'



class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class AnalyticsSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    num_payments = serializers.IntegerField()
    num_active_customers = serializers.IntegerField()
    num_inactive_customers = serializers.IntegerField()
    num_active_devices = serializers.IntegerField()
    num_inactive_devices = serializers.IntegerField()

# class AnalyticsSerializer(serializers.Serializer):
#     total_revenue_today = serializers.DecimalField(max_digits=8, decimal_places=2)
#     total_revenue_yesterday = serializers.DecimalField(max_digits=8, decimal_places=2)
#     total_revenue_last_7_days = serializers.DecimalField(max_digits=8, decimal_places=2)
#     total_revenue_last_30_days = serializers.DecimalField(max_digits=8, decimal_places=2)
#     total_revenue_last_90_days = serializers.DecimalField(max_digits=8, decimal_places=2)
#
#     payments_received_today = serializers.IntegerField()
#     payments_received_yesterday = serializers.IntegerField()
#     payments_received_last_7_days = serializers.IntegerField()
#     payments_received_last_30_days = serializers.IntegerField()
#     payments_received_last_90_days = serializers.IntegerField()
#
#     active_customers = serializers.IntegerField()
#     inactive_customers = serializers.IntegerField()
#
#     active_devices = serializers.IntegerField()
#     inactive_devices = serializers.IntegerField()
#
#     def to_representation(self, instance):
#         data = {
#             'total_revenue_today': Payment.objects.filter(today_filter('payment_date')).aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0,
#             'total_revenue_yesterday': Payment.objects.filter(yesterday_filter('payment_date')).aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0,
#             'total_revenue_last_7_days': Payment.objects.filter(last_7_days_filter('payment_date')).aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0,
#             'total_revenue_last_30_days': Payment.objects.filter(last_30_days_filter('payment_date')).aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0,
#             'total_revenue_last_90_days': Payment.objects.filter(last_90_days_filter('payment_date')).aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0,
#
#             'payments_received_today': Payment.objects.filter(today_filter('payment_date')).count(),
#             'payments_received_yesterday': Payment.objects.filter(yesterday_filter('payment_date')).count(),
#             'payments_received_last_7_days': Payment.objects.filter(last_7_days_filter('payment_date')).count(),
#             'payments_received_last_30_days': Payment.objects.filter(last_30_days_filter('payment_date')).count(),
#             'payments_received_last_90_days': Payment.objects.filter(last_90_days_filter('payment_date')).count(),
#
#             'active_customers': Customer.objects.filter(device__status=Device.ACTIVE).distinct().count(),
#             'inactive_customers': Customer.objects.filter(device__status=Device.NOT_ACTIVE).distinct().count(),
#
#             'active_devices': Device.objects.filter(status=Device.ACTIVE).count(),
#             'inactive_devices': Device.objects.filter(status=Device.NOT_ACTIVE).count(),
#         }
#         return data


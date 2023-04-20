from rest_framework import serializers
from .models import Company, CompanyServiceRelationship,\
    Service,Locality,Customer,\
    Package,Device,Recharge,PaymentMode,Client


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

    def get_fields(self):
        fields = super().get_fields()
        fields['package_count'] = self.package_count
        return fields

    def create(self, validated_data):
        service_ids = validated_data.pop('company_service')
        company_instance = Company.objects.create(**validated_data)

        for service_id in service_ids:
            Service.objects.get
            relationship_instance = CompanyServiceRelationship(
                service_info=service_id,
                company_info=company_instance,
            )
            relationship_instance.save()

        return company_instance


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
    def get_fields(self):
        fields = super().get_fields()
        fields['device_count'] = self.device_count
        fields['customer_count'] = self.customer_count
        return fields


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

class CustomerListSerializer(serializers.ModelSerializer):
    locality = LocalitySerializer(read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'


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
        model = Recharge
        fields = '__all__'



class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
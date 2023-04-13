from rest_framework import serializers
from .models import Company, CompanyServiceRelationship,\
    Service,Locality,Customer,\
    Package,Device,Recharge,PaymentMode,Client

class CompanySerializer(serializers.ModelSerializer):
    company_service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)

    class Meta:
        model = Company
        fields = '__all__'

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

class CompanyServiceRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyServiceRelationship
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class LocalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Locality
        fields = '__all__'



class PackageSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)
    service_name = serializers.CharField(write_only=True)

    class Meta:
        model = Package
        fields = ('id', 'name', 'price_monthly', 'company_name', 'service_name', 'created_at', 'updated_at')

    def create(self, validated_data):
        company_name = validated_data.pop('company_name')
        service_name = validated_data.pop('service_name')

        company = Company.objects.get(company_name=company_name)
        service = Service.objects.get(name=service_name)

        company_service_info = CompanyServiceRelationship.\
            objects.filter(company_info=company, service_info=service).first()
        package = Package.objects.create(company_service_info=company_service_info, **validated_data)
        return package

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class CompanyServiceRelationshipSerializer(serializers.ModelSerializer):
    company_info = CompanySerializer(read_only=True)
    service_info = ServiceSerializer(read_only=True)
    class Meta:
        model = CompanyServiceRelationship
        fields = '__all__'

class PackageALLSerializer(serializers.ModelSerializer):
    company_service_info = CompanyServiceRelationshipSerializer(read_only=True)
    class Meta:
        model = Package
        fields = '__all__'

class DeviceCustomSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    package = PackageALLSerializer(read_only=True)
    class Meta:
        model = Device
        fields = '__all__'

class RechargeSerializer(serializers.ModelSerializer):
    device = DeviceCustomSerializer(read_only=True)

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
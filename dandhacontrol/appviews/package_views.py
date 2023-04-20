from dandhacontrol.models import Package, CompanyServiceRelationship
from dandhacontrol.serializers import PackageSerializer, PackageALLSerializer, PackageListSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from dandhacontrol.filters import PackageFilter
from rest_framework import generics



class PackageList(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PackageFilter




class CreatePackageAPIView(generics.CreateAPIView):
    """This endpoint allows for creation of a Package"""
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class PackageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageALLSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )

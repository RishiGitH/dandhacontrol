from dandhacontrol.models import CompanyServiceRelationship
from dandhacontrol.serializers import CompanySerializer, CompanyServiceRelationshipSerializer, CompanyServiceRelationshipListSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics






class CompanyServiceRelationshipList(generics.ListAPIView):
    queryset = CompanyServiceRelationship.objects.all()
    serializer_class = CompanyServiceRelationshipListSerializer

    # permission_classes = [IsAdminCompany]

class CreateCompanyServiceRelationshipAPIView(generics.CreateAPIView):
    """This endpoint allows for creation of a Company"""
    queryset = CompanyServiceRelationship.objects.all()
    serializer_class = CompanyServiceRelationshipSerializer

class CompanyServiceRelationshipRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyServiceRelationship.objects.all()
    serializer_class = CompanyServiceRelationshipSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )
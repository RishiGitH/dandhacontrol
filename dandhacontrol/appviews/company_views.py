from dandhacontrol.models import Company
from dandhacontrol.serializers import CompanySerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics



class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    # permission_classes = [IsAdminCompany]

class CreateCompanyAPIView(generics.CreateAPIView):
    """This endpoint allows for creation of a Company"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )





# class CompanyViewSet(viewsets.ModelViewSet):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
# class ListCompanyAPIView(ListAPIView):
#     """This endpoint list all of the available Companys from the database"""
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#
# class CreateCompanyAPIView(CreateAPIView):
#     """This endpoint allows for creation of a Company"""
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#
# class UpdateCompanyAPIView(UpdateAPIView):
#     """This endpoint allows for updating a specific Company by passing in the id of the Company to update"""
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#
# class DeleteCompanyAPIView(DestroyAPIView):
#     """This endpoint allows for deletion of a specific Company from the database"""
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#
#
# class CompanyList(generics.ListCreateAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer
#     # permission_classes = [IsAdminCompany]
#
#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = CompanySerializer(queryset, many=True)
#         return Response(serializer.data)
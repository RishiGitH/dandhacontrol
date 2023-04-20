from dandhacontrol.models import Customer
from dandhacontrol.serializers import CustomerSerializer, CustomerListSerializer
from rest_framework import generics




class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )

class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )


class CustomerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )
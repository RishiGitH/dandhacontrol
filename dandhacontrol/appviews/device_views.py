from dandhacontrol.models import Device
from dandhacontrol.serializers import DeviceSerializer, DeviceCustomSerializer
from django_filters.rest_framework import DjangoFilterBackend
from dandhacontrol.filters import DeviceFilter
from rest_framework import generics




class DeviceList(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceCustomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DeviceFilter
    # permission_classes = (IsAuthenticatedOrReadOnly, )



class DeviceCreateView(generics.CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )


class DeviceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )

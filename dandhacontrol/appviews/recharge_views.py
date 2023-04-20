from dandhacontrol.models import Recharge
from dandhacontrol.serializers import RechargeSerializer, RechargeListSerializer
from rest_framework import generics
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django_filters.rest_framework import DjangoFilterBackend
from dandhacontrol.filters import RechargeFilter
from dandhacontrol.appviews import CustomObjectPermission



class RechargeList(generics.ListAPIView):
    queryset = Recharge.objects.all()
    serializer_class = RechargeListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RechargeFilter

    # def get_queryset(self):
    #     client_id = self.request.client_id
    #     queryset = Recharge.objects.filter(device__customer__client__client_auth_id=client_id)
    #
    #     # Filter by recharge date
    #     recharge_date = self.request.query_params.get('recharge_date', None)
    #
    #     if recharge_date is not None:
    #         date_obj = datetime.strptime(recharge_date, "%Y-%m-%d")
    #
    #         new_date_obj = date_obj - relativedelta(months=1) + timedelta(days=1)
    #         new_date_str = new_date_obj.strftime("%Y-%m-%d")
    #         queryset = queryset.filter(device__recharge_date=new_date_str)
    #
    #     # Filter by locality
    #     locality_id = self.request.query_params.get('locality_id', None)
    #     if locality_id is not None:
    #         queryset = queryset.filter(device__locality=locality_id)
    #
    #     return queryset

class RechargeCreateView(generics.CreateAPIView):
    queryset = Recharge.objects.all()
    serializer_class = RechargeSerializer

class RechargeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recharge.objects.all()
    serializer_class = RechargeSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )

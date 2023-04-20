from dandhacontrol.models import Payment
from dandhacontrol.serializers import PaymentSerializer, PaymentListSerializer
from rest_framework import generics
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django_filters.rest_framework import DjangoFilterBackend
from dandhacontrol.filters import PaymentFilter
from dandhacontrol.appviews import CustomObjectPermission



class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

    # def get_queryset(self):
    #     client_id = self.request.client_id
    #     queryset = Payment.objects.filter(device__customer__client__client_auth_id=client_id)
    #
    #     # Filter by Payment date
    #     Payment_date = self.request.query_params.get('Payment_date', None)
    #
    #     if Payment_date is not None:
    #         date_obj = datetime.strptime(Payment_date, "%Y-%m-%d")
    #
    #         new_date_obj = date_obj - relativedelta(months=1) + timedelta(days=1)
    #         new_date_str = new_date_obj.strftime("%Y-%m-%d")
    #         queryset = queryset.filter(device__Payment_date=new_date_str)
    #
    #     # Filter by locality
    #     locality_id = self.request.query_params.get('locality_id', None)
    #     if locality_id is not None:
    #         queryset = queryset.filter(device__locality=locality_id)
    #
    #     return queryset

class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )

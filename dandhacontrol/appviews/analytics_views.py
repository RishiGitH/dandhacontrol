from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from dandhacontrol.models import Customer, Device, Payment
from dandhacontrol.filters import PaymentDateFilter
from dandhacontrol.serializers import AnalyticsSerializer
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

class AnalyticsView(generics.ListAPIView):
    queryset = Payment.objects.all()
    filter_class = PaymentDateFilter
    serializer_class = AnalyticsSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_revenue = queryset.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
        num_payments = queryset.count()

        client_id = self.request.query_params.get('client_id', None)
        if client_id:
            customers = Customer.objects.filter(client_id=client_id)
        else:
            customers = Customer.objects.all()

        num_active_customers = Customer.objects.filter(device__status=Device.ACTIVE).distinct().count()
        num_inactive_customers = Customer.objects.filter(device__status=Device.NOT_ACTIVE).distinct().count()

        num_active_devices = Device.objects.filter(customer__in=customers, status=Device.ACTIVE).count()
        num_inactive_devices = Device.objects.filter(customer__in=customers, status=Device.NOT_ACTIVE).count()

        data = {
            'total_revenue': total_revenue,
            'num_payments': num_payments,
            'num_active_customers': num_active_customers,
            'num_inactive_customers': num_inactive_customers,
            'num_active_devices': num_active_devices,
            'num_inactive_devices': num_inactive_devices,
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data)
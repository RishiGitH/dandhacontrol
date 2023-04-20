"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path,include
from dandhacontrol.appviews.company_views import CompanyList,CreateCompanyAPIView, CompanyRetrieveUpdateDestroyAPIView
from dandhacontrol.appviews.device_views import DeviceRetrieveUpdateDestroyAPIView, DeviceList, DeviceCreateView
from dandhacontrol.appviews.locality_views import LocalityListCreateView, LocalityRetrieveUpdateDestroyAPIView
from dandhacontrol.appviews.package_views import PackageList,CreatePackageAPIView, PackageRetrieveUpdateDestroyAPIView
from dandhacontrol.appviews.payment_mode_views import PaymentModeListCreateView, PaymentModeRetrieveUpdateDestroyAPIView
from dandhacontrol.appviews.recharge_views import RechargeList, RechargeCreateView, RechargeRetrieveUpdateDestroyAPIView
from dandhacontrol.appviews.service_views import ServiceListCreateView, ServiceRetrieveUpdateDestroyAPIView
from dandhacontrol.appviews.customer_views import CustomerList, CustomerCreateView, CustomerRetrieveUpdateDestroyAPIView
from dandhacontrol.appviews.client_views import ClientListCreateView, ClientRetrieveUpdateDestroyAPIView
from dandhacontrol.appviews.company_service_views import  CompanyServiceRelationshipList, \
    CreateCompanyServiceRelationshipAPIView, CompanyServiceRelationshipRetrieveUpdateDestroyAPIView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="dandhacontrol",
        default_version='v1',
        description="Dummy description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@dummy.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


from django.views.decorators.cache import cache_page

urlpatterns = [
    re_path(r'^ht/', include('health_check.urls')),
    path('admin', admin.site.urls),


    path('company/list', CompanyList.as_view()),
    path('company/create', CreateCompanyAPIView.as_view()),
    path('company/<uuid:pk>/', CompanyRetrieveUpdateDestroyAPIView.as_view()),

    path('service', ServiceListCreateView.as_view()),
    path('service/<uuid:pk>/', ServiceRetrieveUpdateDestroyAPIView.as_view()),

    path('customer/list', CustomerList.as_view()),
    path('customer/create', CustomerCreateView.as_view()),
    path('customer/<uuid:pk>/', CustomerRetrieveUpdateDestroyAPIView.as_view()),

    path('device/list', DeviceList.as_view()),
    path('device/create', DeviceCreateView.as_view()),
    path('device/<uuid:pk>/', DeviceRetrieveUpdateDestroyAPIView.as_view()),

    path('locality', LocalityListCreateView.as_view()),
    path('locality/<uuid:pk>/', LocalityRetrieveUpdateDestroyAPIView.as_view()),

    path('package/list', PackageList.as_view()),
    path('package/create', CreatePackageAPIView.as_view()),
    path('package/<uuid:pk>/', PackageRetrieveUpdateDestroyAPIView.as_view()),

    path('company_service_relationship/list', CompanyServiceRelationshipList.as_view()),
    path('company_service_relationship/create', CreateCompanyServiceRelationshipAPIView.as_view()),
    path('company_service_relationship/<uuid:pk>/', CompanyServiceRelationshipRetrieveUpdateDestroyAPIView.as_view()),

    path('payment_mode', PaymentModeListCreateView.as_view()),
    path('payment_mode/<uuid:pk>/', PaymentModeRetrieveUpdateDestroyAPIView.as_view()),

    path('recharge/list', RechargeList.as_view()),
    path('recharge/create', RechargeCreateView.as_view()),
    path('recharge/<uuid:pk>/', RechargeRetrieveUpdateDestroyAPIView.as_view()),

    path('client', ClientListCreateView.as_view()),
    path('client/<uuid:pk>/',ClientRetrieveUpdateDestroyAPIView.as_view()),

    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += [
    re_path(r'^playground/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

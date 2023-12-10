"""
URL configuration for vendor_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# urls.py
from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [  
    # Vendor URLs
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('api/vendors/', views.create_and_list_vendor, name='create_vendor'),
    path('api/vendors/<int:vendor_id>/', views.handle_vendor, name='handle_vendor'),
    
    # Purchase Order (PO) URLs
    path('api/purchase_orders/', views.create_and_list_purchase_order, name='create_purchase_order'),
    path('api/purchase_orders/<int:po_id>/', views.handle_purchase_order, name='handle_purchase_order'),
    

    # Historical Performance
    path('api/vendors/<int:vendor_id>/performance/', views.vendor_performance, name='vendor_performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge_purchase_order'),
    
]


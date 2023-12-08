

from django import forms
from app1.models import Vendor,PurchaseOrder,PerformanceRecord


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
    #     widgets = {
    #         'name' : forms.TextInput(attrs={'class':'form-control'}),
    #         'contact_details' : forms.TextInput(attrs={'class':'form-control'}),
    #         'address' : forms.TextInput(attrs={'class':'form-control'}),
    #         'vendor_code': forms.NumberInput(attrs={'class':'form-control'}), 
    #         'on_time_delivery_rate': forms.NumberInput(attrs={'class':'form-control'}), 
    #         'quality_rating_avg': forms.NumberInput(attrs={'class':'form-control'}), 
    #         'average_response_time': forms.NumberInput(attrs={'class':'form-control'}), 
    #         'fulfillment_rate': forms.NumberInput(attrs={'class':'form-control'}),
    # }


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']


class PerformanceRecordForm(forms.ModelForm):
    class Meta:
        model = PerformanceRecord
        fields = ['vendor','date','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']
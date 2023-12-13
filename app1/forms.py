

from django import forms
from app1.models import Vendor,PurchaseOrder,PerformanceRecord


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 
                  'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
    

class VendorModelChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        return int(value)

class PurchaseOrderForm(forms.ModelForm):
    # Exclude the 'vendor' field from user input
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), required=False)
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor','order_date', 'delivery_date', 'items', 'quantity', 'status',
                  'quality_rating', 'issue_date', 'acknowledgment_date']


class PerformanceRecordForm(forms.ModelForm):
    class Meta:
        model = PerformanceRecord
        fields = ['vendor','date','on_time_delivery_rate','quality_rating_avg',
                  'average_response_time','fulfillment_rate']
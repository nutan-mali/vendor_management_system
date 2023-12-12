from django.shortcuts import HttpResponse
from .forms import VendorForm,PurchaseOrderForm
from app1.models import Vendor,PurchaseOrder,PerformanceRecord
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Avg,F, ExpressionWrapper, fields


@csrf_exempt
def home(request):
    return HttpResponse('This is a Vendor Management System using Django and Django REST Framework.This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.')
 
@csrf_exempt
def create_and_list_vendor(request):
    if request.method == 'POST':          
        print(type(dict(request.POST)))            
        # Print and Check the data in request.POST as a dictionary
        print(dict(request.POST))     
    
        # Load the JSON data from the request body # Loads converts a string to dict and vice versa .dumps
        context = json.loads(request.body)
        print(context)          
        
        # Create a VendorForm instance with the loaded JSON data
        data = VendorForm(context)   
        if data.is_valid():  
            vendor = data.save()        
        # Return a JSON response indicating successful creation
            return JsonResponse({'message': 'Vendor created successfully'}, status=200)     
        else:
            return JsonResponse({'error': 'Invalid data format or type And Vendor Code Must Be unique'}, status=400)        # Return a JSON response with error messages if the form is not valid
    
    elif request.method == 'GET':       
        # Retrieve all data of the Vendor model from the database
        vendor = Vendor.objects.all() 
        print(vendor)
        # # Retrieve and print the values of all instances of the Vendor model. 
        print(Vendor.objects.values()) 
    

        # prints the type of the object resulting from the conversion to a list 
        print(type(list(Vendor.objects.values())))      
         # converts the QuerySet into a list of dictionaries. 
        vendors = list(vendor.values())  
           
    # Return a JSON response containing the list of Vendor instances
        return JsonResponse({'vendor': vendors}, safe=False)    

@csrf_exempt    
def handle_vendor(request, vendor_id):
    if request.method == "GET": 
        # Retrieve the vendor with the specified ID and get all fields as a dictionary
        vendor = Vendor.objects.filter(pk=vendor_id).values().first()       
        print(vendor)  
        if vendor is not None:
        # Return the vendor details as a JSON response
            return JsonResponse(vendor, safe=False)     
        else:
        # Print the retrieved vendor 
            return JsonResponse({'error': 'Vendor not found'}, status=404)        
    elif request.method == 'PUT':
        
            vendor = Vendor.objects.get(pk=vendor_id)
            context = json.loads(request.body)

            # Update specific fields based on the content of the JSON data
            for key, value in context.items():
                setattr(vendor, key, value)

            vendor.save()
            print(f"Updated vendor is : {model_to_dict(vendor)}")
            return JsonResponse({'message': 'Update done!'})
    
    elif request.method == "DELETE":
        vendor = Vendor.objects.filter(pk=vendor_id).first()
        vendor.delete()    
     # Return a JSON response indicating successful deletion
        return JsonResponse({'message': 'Vendor deleted successfully'}) 
     
    else:
    # Return a JSON response indicating that DELETE method is required
        return JsonResponse({'error': 'Method Not Allowed'}, status=400) 
             
    
@csrf_exempt 
def create_and_list_purchase_order(request):
    
    if request.method == 'POST':
        # loads the JSON data and converts string to dict
        context = json.loads(request.body)    
        print(context)
        #creates a PurchaseOrderForm instance with the loaded JSON data.
        data = PurchaseOrderForm(context)   

        if data.is_valid():
            order = data.save()
            return JsonResponse({'message': 'Purchase Order created successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid data format or type', 'errors': data.errors}, status=400)

    elif request.method == 'GET':
        # Retrieve all fields of the PurchaseOrder model from the database
        orders = PurchaseOrder.objects.all()    
         # orders
        print(orders,'testing on line 84')     
        # Convert the queryset into a list of dictionaries containing fields and values
        order_data = list(orders.values())      
        print(order_data)                        
        return JsonResponse({'orders': order_data}, safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt 
def handle_purchase_order(request,po_id):
    if request.method == 'GET':
        # Retrieve the vendor with the specified ID and get all fields as a dictionary
        order = PurchaseOrder.objects.filter(pk=po_id).values().first()       
         # Print the retrieved vendor 
        print(order)      
        if order is not None:
        # Return the vendor details as a JSON response
            return JsonResponse(order, safe=False)     
        else:
        # Return an error response
            return JsonResponse({'error': 'order not found'}, status=404)   

    elif request.method == 'PUT':
        order = PurchaseOrder.objects.get(pk=po_id)
        context = json.loads(request.body) 
       
        # Assuming 'vendor' is a key in the JSON payload
        vendor_id = context.get('vendor', None)
        if vendor_id is not None:
            vendor_instance = Vendor.objects.get(pk=vendor_id)
             # Set the vendor_id in the PurchaseOrder instance
            order.vendor = vendor_instance
        for key,value in context.items():
            # Skip updating the 'vendor' field directly
            if key == 'vendor':  
                        continue
            
            setattr(order,key,value) 
        order.save()
        print(f"Updated Purchase Order is :{model_to_dict(order)}")
        return JsonResponse({'message': 'Purchase Order Update done!'})
    
    elif request.method == 'DELETE':
        order = PurchaseOrder.objects.filter(pk=po_id).first()
        order.delete()    
    # Return a JSON response indicating successful deletion
        return JsonResponse({'message': 'Order deleted successfully'})  
    else:
        return JsonResponse({'error': 'DELETE method is required'}, status=400)
    
 
# On-Time Delivery Rate
    # When: Each time a Purchase Order (PO) status changes to 'completed'.
    # Here calculate the no of PO which are delieverd on or before the delebery_date.
    # Then: devide this count by The total no of completed POs for that vendor.
def cal_on_time_delivery_rate(vendor):
    
    completed_po = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    print("complete POs ",completed_po)
    # __lte (less than or equal to) lookup and the F object to reference the acknowledgment_date field.
    # Here __lte checks delivery_date is <= acknowledgment_date.
    # count() giving the count of completed purchase orders that meet the specified condition. 
    on_time_delivery = completed_po.filter(delivery_date__lte=F('acknowledgment_date')).count()
    print("On time deliverys " ,on_time_delivery)
    total_completed_po = completed_po.count()
    print("total completed Pos " ,total_completed_po)
    
    # Calculate the on-time delivery rate based on the count of completed purchase orders
    # delivered on time (on_time_delivery) and the total count of completed purchase orders (total_completed_po).
    # Avoid division by zero by setting on_time_delivery_rate to 0 if total_completed_po is not greater than 0.

    on_time_delivery_rate = on_time_delivery / total_completed_po if total_completed_po > 0 else 0
    vendor.on_time_delivery_rate = vendor.on_time_delivery_rate
    vendor.save()

# # Quality Rating Average
# def cal_quality_rating_average(vendor):
#     completed_po = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
#     quality_rating_avg = completed_po.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
#     vendor.quality_rating_avg = quality_rating_avg
#     vendor.save()

# # Average Response Time
# def cal_average_response_time(vendor):
#     completed_po = PurchaseOrder.objects.filter(vendor=vendor, status='completed', acknowledgment_date__isnull=False)
#     avg_response_time = completed_po.aggregate(avg_rating=Avg(F('acknowledgment_date') - F('issue_date')))['acknowledgment_date__avg'] or 0
#     vendor.average_response_time = avg_response_time.total_seconds() / 60  # Convert to minutes
#     vendor.save()

# # Fulfilment Rate
# def cal_fulfilment_rate(vendor):
#     total_po = PurchaseOrder.objects.filter(vendor=vendor)
#     successfully_fulfilled_pos = total_po.filter(status='completed', issues__isnull=True).count()
#     fulfilment_rate = successfully_fulfilled_pos / total_po.count() if total_po.count() > 0 else 0
#     vendor.fulfilment_rate = fulfilment_rate
#     vendor.save()


@csrf_exempt 
def acknowledge_purchase_order(request, po_id):
    pass

@csrf_exempt 
def vendor_performance(request, vendor_id):
    pass
#     try:
#         vendor = Vendor.objects.get(pk=vendor_id)
#     except Vendor.DoesNotExist:
#         return JsonResponse({'error': 'Vendor not found'}, status=404)

#     # Call the functions to calculate performance metrics
#     cal_on_time_delivery_rate(vendor)
#     cal_quality_rating_average(vendor)
#     cal_average_response_time(vendor)
#     cal_fulfilment_rate(vendor)

#     # Return the calculated metrics as a JSON response
#     return JsonResponse({
#         'on_time_delivery_rate': vendor.on_time_delivery_rate,
#         'quality_rating_avg': vendor.quality_rating_avg,
#         'average_response_time': vendor.average_response_time,
#         'fulfilment_rate': vendor.fulfilment_rate
#     })


    





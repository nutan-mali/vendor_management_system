from django.shortcuts import HttpResponse,get_object_or_404
from django.utils import timezone
from .forms import VendorForm,PurchaseOrderForm
from app1.models import Vendor,PurchaseOrder,PerformanceRecord
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict



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
            return JsonResponse(vendor, safe=False)   #safe=False is provide more flexibility for using data that contains complex structure  such as dictionaries with non-string keys (e.g., integers).
        # This setting is useful when more complex data structures that need to be converted to JSON.   
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
        # Check if vendor_id is provided
        vendor_id = context.get('vendor_id', None)
        print(f"Vendor ID received: {vendor_id}")
        if vendor_id is None:
            return JsonResponse({'error': 'Vendor ID is required for creating a purchase order'}, status=400)
        try:
            # Retrieve the Vendor instance based on vendor_id
            vendor_instance = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return JsonResponse({'error': 'Vendor not found'}, status=404)
        
        #creates a PurchaseOrderForm instance with the loaded JSON data.
        data = PurchaseOrderForm(context)   

        if data.is_valid():
            # Manually set the 'vendor' field before saving
            data.instance.vendor = vendor_instance
            data.save()
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
        # Retrieve the PurchaseOrder instance with the specified primary key (po_id)
# If the PurchaseOrder does not exist, raise a 404 response
        order = get_object_or_404(PurchaseOrder, pk=po_id)

        order_data = model_to_dict(order)       
         # Print the retrieved vendor 
        print(order)      
        if order is not None:
        # Return the vendor details as a JSON response
            return JsonResponse(order_data, safe=False)     
        else:
        # Return an error response
            return JsonResponse({'error': 'order not found'}, status=404)   

    elif request.method == 'PUT':
        # Retrieve the PurchaseOrder instance with the specified primary key (po_id)
# If the PurchaseOrder does not exist, raise a 404 response
        order = get_object_or_404(PurchaseOrder, pk=po_id)
        # Convert the PurchaseOrder instance to a dictionary using model_to_dict
        context = json.loads(request.body) 
       
        # Assuming 'vendor' is a key in the JSON payload
        vendor_id = context.get('vendor_id', None)
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
    vendor_id = vendor.id
    print("Vendor ID:", vendor_id)
    completed_po = vendor.purchase_orders.filter(status='completed', acknowledgment_date__isnull=False)
    print("Complete POs:", completed_po)
     # Initialize counters for on-time deliveries and total completed purchase orders
    on_time_deliveries = 0
    total_completed_po = 0

    # Iterate through completed purchase orders
    for po in completed_po:
        # Check if the delivery date is on or before the acknowledgment date
        if po.delivery_date <= po.acknowledgment_date:
            on_time_deliveries += 1
        total_completed_po += 1
    print("On-Time Deliveries:", on_time_deliveries)
    print("Total Completed POs:", total_completed_po)

    # Calculate the on-time delivery rate
    on_time_delivery_rate = on_time_deliveries / total_completed_po if total_completed_po > 0 else 0

    # Update and save the on-time delivery rate in the vendor instance
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.save()

    return vendor.on_time_delivery_rate
    

# # Quality Rating Average
def cal_quality_rating_avg(vendor):
    completed_po = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    # Initialize the total and count variables to calculate the average
    total_quality_rating = 0
    count = 0

# Loop through each completed purchase order
    for po in completed_po:
    # Check if the quality rating is not None (not null)
        if po.quality_rating is not None:
        # Add the quality rating to the total
            total_quality_rating += po.quality_rating
        # Increment the count
            count += 1

# Calculate the average quality rating or set to 0 if there are no ratings
    quality_rating_avg = total_quality_rating / count if count > 0 else 0

# Now, quality_rating_avg contains the average quality rating or 0 if there are no ratings
    # quality_rating_avg = completed_po.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
    vendor.quality_rating_avg = quality_rating_avg
    vendor.save()
    return vendor.quality_rating_avg
# # Average Response Time
def cal_average_response_time(vendor):
    # Assume vendor.purchase_orders is a related manager for PurchaseOrder instances
    
    # Get completed purchase orders with acknowledgment dates for the vendor
    completed_po = vendor.purchase_orders.filter(status='completed', acknowledgment_date__isnull=False)
    
    # Initialize total response time and count variables
    total_response_time = 0
    count = 0
    
    # Loop through each completed purchase order
    for po in completed_po:
        # Calculate the response time for each purchase order
        response_time = po.acknowledgment_date - po.issue_date
        # Add the response time to the total
        total_response_time += response_time.total_seconds()
        # Increment the count
        count += 1
    
    # Calculate the average response time (in minutes) or set to 0 if there are no responses
    avg_response_time = total_response_time / 60 / count if count > 0 else 0
    
    # Set the average response time in the vendor instance
    vendor.average_response_time = avg_response_time
    
    # Save the updated vendor instance to the database
    vendor.save()
    return vendor.average_response_time


def cal_fulfillment_rate(vendor):
    # Assume vendor.purchase_orders is a related manager for PurchaseOrder instances

    # Get all purchase orders for the vendor
    all_purchase_orders = vendor.purchase_orders.all()
    print("All Purchase Orders:", all_purchase_orders)
    # Calculate the total number of purchase orders
    total_purchase_orders_count = all_purchase_orders.count()
    print("Total Purchase Orders Count:", total_purchase_orders_count)
    # Calculate the number of successfully fulfilled purchase orders
    successfully_fulfilled_count = all_purchase_orders.filter(status='completed').count()
    print("Successfully Fulfilled Count:", successfully_fulfilled_count)

    # Calculate the fulfillment rate or set to 0 if there are no purchase orders
    fulfillment_rate = 0 if total_purchase_orders_count == 0 else successfully_fulfilled_count / total_purchase_orders_count
    print("Calculated Fulfillment Rate:", fulfillment_rate)
    # Set the fulfillment rate in the vendor instance
    vendor.fulfillment_rate = fulfillment_rate

    # Save the updated vendor instance to the database
    vendor.save()
    return fulfillment_rate


@csrf_exempt 
def vendor_performance(request, vendor_id):
     # Retrieve the vendor instance or return a 404 response if not found
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    
    on_time_delivery_rate = cal_on_time_delivery_rate(vendor)
    print(vendor.on_time_delivery_rate)
    quality_rating_avg = cal_quality_rating_avg(vendor)
    print(vendor.quality_rating_avg)
    average_response_time = cal_average_response_time(vendor)
    print(vendor.average_response_time)
    fulfillment_rate  = cal_fulfillment_rate(vendor)
    print(vendor.fulfillment_rate)
    
    performance_record = PerformanceRecord(
        vendor=vendor,
        date=timezone.now(),  # Set the date to the current time or adjust as needed
        on_time_delivery_rate=on_time_delivery_rate,
        quality_rating_avg=quality_rating_avg,
        average_response_time=average_response_time,
        fulfillment_rate=fulfillment_rate
    )

    # Save the PerformanceRecord instance to the database
    performance_record.save()
    # Return the calculated metrics in a JSON response
    performance_data = {
        
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfillment_rate': fulfillment_rate,
    }
    print(performance_data)

    return JsonResponse(performance_data)
    

@csrf_exempt
def acknowledge_purchase_order(request, po_id):
    # Retrieve the PurchaseOrder instance with the specified primary key (po_id)
    order = get_object_or_404(PurchaseOrder, pk=po_id)

    if request.method == 'POST':
        # Check if the purchase order is not already acknowledged
        if order.acknowledgment_date is not None:
            return JsonResponse({'error': 'Purchase Order already acknowledged'}, status=400)

        # Perform the acknowledgment
        order.acknowledgment_date = timezone.now()  # Assuming you have imported timezone
        order.save()

        # Recalculate the average response time after acknowledgment
        vendor = order.vendor
        vendor.average_response_time = cal_average_response_time(vendor)
        vendor.save()

        return JsonResponse({'message': 'Purchase Order acknowledged successfully'}, status=200)
    else:
        # Return a JSON response indicating that the method is not allowed
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    





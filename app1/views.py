from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from .models import Vendor
from .forms import VendorForm,PurchaseOrderForm
from app1.models import Vendor,PurchaseOrder
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

def home(request):
    return HttpResponse('This is a Vendor Management Systemusing Django and Django REST Framework.This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.')
 
@csrf_exempt
def create_and_list_vendor(request):
    if request.method == 'POST':          
        print(type(dict(request.POST)))            
        print(dict(request.POST))      # Print and Check the data in request.POST as a dictionary
    
        context = json.loads(request.body)      # Load the JSON data from the request body
        print(context)          
        
        data = VendorForm(context)       # Create a VendorForm instance with the loaded JSON data
        if data.is_valid():  
            vendor = data.save()        
            return JsonResponse({'message': 'Vendor created successfully'}, status=200)     # Return a JSON response indicating successful creation
        else:
            return JsonResponse({'error': 'Invalid data format or type And Vendor Code Must Be unique'}, status=400)        # Return a JSON response with error messages if the form is not valid
    
    elif request.method == 'GET':       
        vendor = Vendor.objects.all() # Retrieve all data of the Vendor model from the database
        print(Vendor.objects.values())  # Print the values 
        print(type(list(Vendor.objects.values())))      
        vendors = list(vendor.values())      #convert queryset to dict
           
        return JsonResponse({'vendor': vendors}, safe=False)    # Return a JSON response containing the list of Vendor instances

@csrf_exempt    
def retrieve_vendor(request,vendor_id):
    if request.method == "GET":     
        vendor = Vendor.objects.filter(pk=vendor_id).values().first()       # Retrieve the vendor with the specified ID and get all fields as a dictionary
        print(vendor)       # Print the retrieved vendor 
        if vendor is not None:
            return JsonResponse(vendor, safe=False)     # Return the vendor details as a JSON response
        else:
            return JsonResponse({'error': 'Vendor not found'}, status=404)   # Return an error response
    return JsonResponse({'error': 'Method not allowed'}, status=405)        # Return an error response for any method other than GET
    
    #     if vendor is not None:
    #         context = {
    #             'id': vendor.id,
    #             'name': vendor.name,
    #             'contact_details': vendor.contact_details,
    #             'address': vendor.address,
    #             'vendor_code': vendor.vendor_code,
    #             'on_time_delivery_rate': vendor.on_time_delivery_rate,
    #             'quality_rating_avg': vendor.quality_rating_avg,
    #             'average_response_time': vendor.average_response_time,
    #             'fulfillment_rate': vendor.fulfillment_rate,
    #         }
    #         print(context)
    #         return JsonResponse(context, safe=False)
    #     else:
    #         return JsonResponse({'error': 'Vendor not found'}, status=404)

@csrf_exempt    
def update_vendor(request, vendor_id):
    if request.method == 'PUT':
        vendor = Vendor.objects.filter(pk=vendor_id).values().first()
        print(vendor)
        context = json.loads(request.body)
        print(type(context))
        return JsonResponse({'message': 'updation in progress'})
        
       
            
@csrf_exempt  
def delete_vendor(request, vendor_id):
     if request.method == "DELETE":
        vendor = Vendor.objects.filter(pk=vendor_id).first()
        vendor.delete()    
        return JsonResponse({'message': 'Vendor deleted successfully'})  # Return a JSON response indicating successful deletion
     
     else:
        return JsonResponse({'error': 'DELETE method is required'}, status=400) # Return a JSON response indicating that DELETE method is required
        
        
    
@csrf_exempt 
def create_and_list_purchase_order(request):
    
    if request.method == 'POST':
        context = json.loads(request.body)    # loads the JSON data  
        print(context)
        data = PurchaseOrderForm(context)   #creates a PurchaseOrderForm instance with the loaded JSON data.

        if data.is_valid():
            order = data.save()
            return JsonResponse({'message': 'Purchase Order created successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid data format or type', 'errors': data.errors}, status=400)

    elif request.method == 'GET':
        orders = PurchaseOrder.objects.all()    # Retrieve all fields of the PurchaseOrder model from the database
        print(orders)
        order_data = list(orders.values())      # Convert the queryset into a list of dictionaries containing fields and values
        print(order_data)
        return JsonResponse({'orders': order_data}, safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt 
def retrieve_purchase_order(request,po_id):
    if request.method == 'GET':
        order = PurchaseOrder.objects.filter(pk=po_id).values().first()       # Retrieve the vendor with the specified ID and get all fields as a dictionary
        print(order)       # Print the retrieved vendor 
        if order is not None:
            
            return JsonResponse(order, safe=False)     # Return the vendor details as a JSON response
        else:
            return JsonResponse({'error': 'order not found'}, status=404)   # Return an error response
    return JsonResponse({'error': 'Method not allowed'}, status=405)  

@csrf_exempt 
def delete_purchase_order(request,po_id):
    if request.method == 'DELETE':
        order = PurchaseOrder.objects.filter(pk=po_id).first()
        order.delete()    
        return JsonResponse({'message': 'Order deleted successfully'})  # Return a JSON response indicating successful deletion
    else:
        return JsonResponse({'error': 'DELETE method is required'}, status=400)

@csrf_exempt 
def update_purchase_order(request):
    if request.method == 'PUT':
        pass



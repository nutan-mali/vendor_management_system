Vendor Management System with Performance Metrics

Overview
This repository contains the source code for a Vendor Management System with Performance Metrics. The system is built using Django and Django REST Framework, providing a robust solution for handling vendor profiles, purchase order tracking, and calculating vendor performance metrics.




1. Vendor Profile Management

API Endpoints
POST /api/vendors/: Create a new vendor.
GET /api/vendors/: List all vendors.
GET /api/vendors/{vendor_id}/: Retrieve details of a specific vendor.
PUT /api/vendors/{vendor_id}/: Update a vendor's information.
DELETE /api/vendors/{vendor_id}/: Delete a vendor.


2. Purchase Order Tracking


API Endpoints
POST /api/purchase_orders/: Create a new purchase order.
GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.
GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
PUT /api/purchase_orders/{po_id}/: Update a purchase order.
DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.

3. Vendor Performance Evaluation

API Endpoints
GET /api/vendors/{vendor_id}/performance : Retrieve a vendor's performance metrics.

:

Retrieves the calculated performance metrics for a specific vendor.
Should return data including on_time_delivery_rate, quality_rating_avg, average_response_time, and fulfillment_rate.
Update Acknowledgment Endpoint (POST /api/purchase_orders/{po_id}/acknowledge):

While not explicitly detailed in the previous sections, consider an endpoint for vendors to acknowledge POs.
This endpoint will update acknowledgment_date and trigger the recalculation of average_response_time.
Installation
Clone the repository: git clone https://github.com/nutan-mali/vendor_management_system
Navigate to the project directory: cd your-repo
Install dependencies: pip install -r requirements.txt
Apply migrations: python manage.py migrate
Run the development server: python manage.py runserver

Usage
Access the API documentation at http://localhost:8000/docs/ for detailed information on available endpoints and their usage.

Vendor Management System with Performance Metrics
Overview
This repository contains the source code for a Vendor Management System with Performance Metrics. The system is built using Django and Django REST Framework, providing a robust solution for handling vendor profiles, purchase order tracking, and calculating vendor performance metrics.

Objective
The primary goal of this project is to create a comprehensive Vendor Management System that enables efficient vendor profile management, purchase order tracking, and performance metric calculations.

Core Features
1. Vendor Profile Management
Model Design
The system includes a well-defined model to store vendor information, encompassing essential details such as name, contact information, address, and a unique vendor code.

API Endpoints
POST /api/vendors/: Create a new vendor.
GET /api/vendors/: List all vendors.
GET /api/vendors/{vendor_id}/: Retrieve details of a specific vendor.
PUT /api/vendors/{vendor_id}/: Update a vendor's information.
DELETE /api/vendors/{vendor_id}/: Delete a vendor.
2. Purchase Order Tracking
Model Design
Purchase orders are tracked using a comprehensive model that includes fields such as PO number, vendor reference, order date, items, quantity, and status.

API Endpoints
POST /api/purchase_orders/: Create a new purchase order.
GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.
GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
PUT /api/purchase_orders/{po_id}/: Update a purchase order.
DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
3. Vendor Performance Evaluation
Metrics
On-Time Delivery Rate: Percentage of orders delivered by the promised date.
Quality Rating: Average of quality ratings given to a vendor’s purchase orders.
Response Time: Average time taken by a vendor to acknowledge or respond to purchase orders.
Fulfilment Rate: Percentage of purchase orders fulfilled without issues.
Model Design
Fields are added to the vendor model to store these performance metrics.

API Endpoints
GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance metrics.
API Endpoint Implementation
Vendor Performance Endpoint (GET /api/vendors/{vendor_id}/performance):

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

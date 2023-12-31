**#Vendor_Management_System_**


## Overview

The Vendor Management System is a Django-based web application designed to streamline vendor management, purchase order tracking, and historical performance analysis.

## Features

- **Vendor Management:**
  - Easily add, view, update, and delete vendor information.
  
- **Purchase Order Management:**
  - Seamlessly manage purchase orders with features for adding, viewing, updating, and deleting orders.
  - Intelligent date validation ensures the accuracy of order timelines.

- **Historical Performance:**
  - Automatic tracking of historical performance metrics for vendors.
  - Metrics include average response time, on-time delivery rate, quality rating average, and fulfillment rate.

- **Acknowledgment:**
  - Vendors can acknowledge purchase orders with a specific acknowledgment date.

- **Token-based Authentication:**
  - Enhance security by implementing token-based authentication for API endpoints. Using DRF's own inbuilt Authentication System.
  ```bash
  curl -X POST http://your-api-domain/api-token-auth/ -d "username=<your-username>&password=<your-password>"
    ```
A token will be generated
Use the token to access the Endpoints. Before that create a User in the shell :

```python copy
>>>from django.contrib.auth.models import User
>>> user = User.objects.create_user('username', 'sample@gmail.com', 'password')               
>>> exit()

#after this (if using POSTMAN send use the username and password to generate the token for the endpoints.
{
    "username" : "username",
    "password" : "password"
}

```

- ## Requirements

- **Python 3.x**
- **Django 4.2.7**: A high-level Python web framework for building web applications.
- **Django REST framework 3.14.0**: A powerful and flexible toolkit for building Web APIs in Django.
- **pytz 2023.3.post1**: World timezone definitions for Python.
- **sqlparse 0.4.4**: A non-validating SQL parser for Python.
- **tzdata 2023.3**: Time zone database for Python.

## Performance Metrics Algorithm

- **Quality Rating Average:**
  - Calculate the average quality rating for completed purchase orders.

- **Average Response Time:**
  - Calculate the average response time from acknowledgment to issue date for acknowledged purchase orders.

- **Fulfillment Rate:**
  - Calculate the fulfillment rate based on completed orders.

- **On-Time Delivery Rate:**
  - Calculate the on-time delivery rate for completed orders.
 
  ## API Endpoints
**Vendors**

1.Add/Get Vendors
```bash
Endpoint: /api/vendors/
Method: GET (Retrieve all vendors), POST (Add a new vendor)
Authentication: Required
```

2.Get/Update/Delete Vendor
```bash
Endpoint: /api/vendors/<vendor_id>/
Method: GET (Retrieve a specific vendor), POST (Update a specific vendor), DELETE (Delete a specific vendor)
Authentication: Required
Parameters: <vendor_id> (string, required): ID of the vendor to retrieve, update, or delete
```

**Purchase Orders**

1.Add/Get Purchase Orders
```bash
Endpoint: /api/purchase_orders/
Method: GET (Retrieve all purchase orders), POST (Add a new purchase order)
Authentication: Required
```

2.Get/Update/Delete Purchase Order
```bash
Endpoint: /api/purchase_orders/<po_id>/
Method: GET (Retrieve a specific purchase order), POST (Update a specific purchase order), DELETE (Delete a specific purchase order)
Authentication: Required
Parameters: <po_id> (string, required): ID of the purchase order to retrieve, update, or delete
```

**Historical Performance**
Get Purchase Orders
Retrieve all purchase orders or add a new purchase order.
``` bash
GET /api/purchase_orders/
Method: GET (Retrieve all historical Performance of the Vendor)
Authentication : Required
```

**Acknowledge Purchase Order**
Parameters:
po_id (string, required): Purchase Order ID, uniquely identifying the purchase order to be acknowledged.
acknowledgment_date (datetime, required): The date and time when the vendor acknowledges the purchase order.
```bash
Endpoint: /api/purchase_orders/<str:po_id>/acknowledge/
Method: POST
Authentication: Required
```
Example Request:

```bash
curl -X POST http://your-api-domain/api/purchase_orders/<your-po-id>/acknowledge/ -d "acknowledgment_date=<acknowledgment-date>"
```
Replace <your-po-id> with the actual Purchase Order ID and <acknowledgment-date> with the date and time of acknowledgment.


## Validation
Included Validation Logic to Each Model and also added Business Logic to the datas created and checked for data integrity.
``` python copy
if not (order_date < delivery_date and acknowledgment_date < delivery_date and issue_date > order_date and acknowledgment_date > issue_date):
            raise serializers.ValidationError("Problem with Dates, Check all the Dates Accordingly")
```

## Command Lines Used: 

Certainly! Below are the commands with brief explanations for each step in running the Django project:

Create Virtual Environment:

```bash
python -m venv [env_name]
```
This command creates a virtual environment named [env_name] to isolate project dependencies.

Activate Virtual Environment:
```bash
. [env_name]/Scripts/activate  # On Windows
source [env_name]/bin/activate  # On macOS/Linux
```
Activates the virtual environment, ensuring that subsequent Python and pip commands use the environment.

Install Django:

```bash
pip install django
```
Installs the Django framework, providing the necessary tools to build and run the web application.

```bash
pip install djangorestframework
```
Installs the Django Rest Framework, an extension for Django that simplifies the creation of RESTful APIs.

Run Tests:


```bash
python manage.py test main_app
```

Executes tests defined in the 'main_app' application to ensure the correctness of the implemented functionality.

Run Development Server:

```bash
python manage.py runserver
```

Starts the Django development server, allowing you to preview and interact with the application locally.

Feel free to replace [env_name] with your desired environment name.

## Additions

The Estimated Delivery Date has been considered to be 7 days after the Order Date. Based on that the delivery performance has been calculated. Feel free to Reach Out to be in case of any query.




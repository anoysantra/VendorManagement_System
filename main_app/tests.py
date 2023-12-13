from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import datetime
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class VendorManagementTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # Create a user and obtain the token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_vendor_crud_operations(self):
        # Add Vendor
        response = self.client.post(reverse('vendor_add_get'), {
                                    'name': 'TestVendor', 'contact_details': 'Contact', 'address': 'Address', 'vendor_code': 'VKV001'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        vendor_id = response.data['id']

        # Get Vendor
        response = self.client.get(
            reverse('vendor_get_update_delete', args=[vendor_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_purchase_order_crud_operations(self):
        #vendor_id = 1
        vendor_response = self.client.post(reverse('vendor_add_get'), {
            'name': 'TestVendor', 'contact_details': 'Contact', 'address': 'Address', 'vendor_code': 'VKV001'})
        vendor_id = vendor_response.data['id']



        # Add Purchase Order
        response = self.client.post(reverse('po_add_get'), {'po_number': 'POV001', 'vendor': vendor_id, 'order_date': '2023-12-01T10:00:00Z', 'delivery_date': '2023-12-10T10:00:00Z',
                                    'items': '[{"item": "Product1", "quantity": 5}]', 'quantity': 5, 'quality_rating' : '4' ,'status': 'completed', 'issue_date': '2023-12-02T10:00:00Z',
                                                            'acknowledgment_date': '2023-12-03T10:00:00Z'})
        print("Test Results: ",response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        po_id = response.data['id']
        print("Po Id:", po_id)

        # Get Specific Purchase Order
        response = self.client.get(
            reverse('po_get_update_delete', args=[po_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #updating a PO
        response = self.client.post(                          
             reverse('po_get_update_delete', args=[po_id]), {'po_number': 'POV001', 'vendor': vendor_id, 'order_date': '2023-12-01T10:00:00Z', 'delivery_date': '2023-12-10T10:00:00Z',
                                    'items': '[{"item": "Product1", "quantity": 5}]', 'quantity': 15, 'quality_rating' : '4' ,'status': 'completed', 'issue_date': '2023-12-02T10:00:00Z',
                                                            'acknowledgment_date': '2023-12-05T10:00:00Z'})
                   
        print(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from datetime import timedelta, timezone, datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from rest_framework import status, serializers
from django.db.models import Avg, Count, F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Vendors
# ..................................................................................................................................

@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_get_vendor(request):

    if request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)


@api_view(['POST', 'GET', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_update_delete_vendor(request, vendor_id):

    vendor = get_object_or_404(Vendor, pk=vendor_id)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = VendorSerializer(instance=vendor, data=request.data)
        vendor = serializer.instance
        print(vendor.address)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        vendor.delete()
        return Response(status=204)


# PurchaseOrder
# ........................................................................................................................

# write code to include date logic in add and update field for purchase order specially the dates

def po_validation(data):

    order_date = datetime.fromisoformat(str(data['order_date']))
    delivery_date = datetime.fromisoformat(str(data['delivery_date']))
    issue_date = datetime.fromisoformat(str(data['issue_date']))
    acknowledgment_date = data.get('acknowledgment_date')

    if acknowledgment_date is not None:
        acknowledgment_date = datetime.fromisoformat(str(data['acknowledgment_date']))
        if not (order_date < delivery_date and acknowledgment_date < delivery_date and issue_date > order_date and acknowledgment_date > issue_date):
            raise serializers.ValidationError("Problem with Dates, Check all the Dates Accordingly")
    else:
        if not (order_date < delivery_date and issue_date > order_date):
            raise serializers.ValidationError("Problem with Dates of Order/Delivery/Issue Date")


@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_get_po(request):

    if request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)

        if serializer.is_valid():
            po_validation(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        purchases = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchases, many=True)
        return Response(serializer.data)


@api_view(['POST', 'GET', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_update_delete_po(request, po_id):

    purchase = get_object_or_404(PurchaseOrder, pk=po_id)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PurchaseOrderSerializer(instance=purchase, data=request.data)
        if serializer.is_valid():
            po_validation(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        purchase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ..........................................................................................................................................
# Historical Performance

@receiver(post_save, sender=PurchaseOrder)
def performance(sender, instance, created, **kwargs):

    vendor = instance.vendor
    issue_date = instance.issue_date

    # Quality Rating Average
    if instance.quality_rating:
        completed_with_rating = PurchaseOrder.objects.filter( vendor=vendor, status='completed', quality_rating__isnull=False)
        quality_ratings = [po.quality_rating for po in completed_with_rating]
        avg_rating = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0
        vendor.quality_rating_avg = avg_rating

    # Average Response Time
    if instance.acknowledgment_date:
        acknowledged_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        response_times = [(po.acknowledgment_date-po.issue_date).total_seconds() for po in acknowledged_orders]
        avg_response_timing = sum(response_times)/len(acknowledged_orders) if response_times else 0
        vendor.average_response_time = avg_response_timing

    # Fulfillment Rate
    total_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    total_purchase_order_for_vendor = PurchaseOrder.objects.filter(vendor=vendor).count()
    total_fulfillment_rate = total_completed_orders /total_purchase_order_for_vendor if total_purchase_order_for_vendor else 0
    vendor.fulfillment_rate = total_fulfillment_rate

    # On-Time Delivery Rate
    if instance.status == 'completed':
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_po_count = completed_orders.count()

        if total_completed_po_count > 0:
            on_time_delivery_count = 0
            standard_delivery_days = 7

            for po in completed_orders:
                estimated_delivery_date = po.order_date + timedelta(days=standard_delivery_days)

                if po.delivery_date <= estimated_delivery_date:
                    on_time_delivery_count = on_time_delivery_count+1

            on_time_delivery_rate = on_time_delivery_count/total_completed_po_count
            vendor.on_time_delivery_rate = on_time_delivery_rate

        else:
            vendor.on_time_delivery_rate = 0

    # Saving the datas to HistoricalPerformance model
    try:
        HistoricalPerformance.objects.create(
            vendor=vendor,
            date=issue_date,
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=avg_rating,
            average_response_time=avg_response_timing,
            fulfillment_rate=total_fulfillment_rate
        )
    except:
        print('Historical Data Not Created.')

    # save the vendor instance
    vendor.save()

# Logging the Historical Performance of a Particular Vendor

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_historical_logs(request, vendor_id):

    data_logs = HistoricalPerformance.objects.filter(vendor=vendor_id)
    serializer = HistoricalPerformanceSerializer(data_logs, many=True)
    return Response(serializer.data)

# .............................................................................................................................................................
# This is For the User to Acknowledge the Purchase Order.Endpoint for vendors to acknowledge a purchase order.

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
   
    # Get acknowledgment date from request data
    acknowledgment_date_str = request.data.get('acknowledgment_date')
    # Validate and parse user input
    try:
        acknowledgment_date = datetime.strptime(acknowledgment_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        return HttpResponse('Invalid acknowledgment date format.', status=400)

    # Update acknowledgment date
    purchase_order.acknowledgment_date = acknowledgment_date
    purchase_order.save()

    return HttpResponse('Purchase order acknowledged successfully.', status=200)

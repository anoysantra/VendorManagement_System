from django.urls import path
from . import views

urlpatterns = [
    path('vendors/', views.add_get_vendor, name='vendor_add_get'),
    path('vendors/<str:vendor_id>', views.get_update_delete_vendor,name='vendor_get_update_delete'),

    path('purchase_orders/', views.add_get_po, name='po_add_get'),
    path('purchase_orders/<str:po_id>', views.get_update_delete_po, name='po_get_update_delete'),
    path('purchase_orders/<str:po_id>/acknowledge/', views.acknowledge_purchase_order, name='ack_purchase_order'),

    path('vendors/<str:vendor_id>/performances/',views.get_historical_logs, name='historical_data'),


]

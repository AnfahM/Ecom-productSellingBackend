# adminside/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard-data/', DashboardDataView.as_view(), name='dashboard-data'),
    path('logo/', LogoView.as_view(), name='logo'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),  # List all customers with is_customer=True
    path('customers/<int:id>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('categories/', CategoryAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryAPIView.as_view(), name='category-delete'),
]
    
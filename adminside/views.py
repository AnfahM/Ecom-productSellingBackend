# adminside/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.models import Customer, Product  # Importing models from myapp
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *
from django.http import Http404

class DashboardDataView(APIView):
    # Add permission classes to ensure only authenticated users can access this view
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Count the total number of customers and products
        total_customers = Customer.objects.count()
        total_products = Product.objects.count()

        # Return the data in a JSON response
        data = {
            'total_customers': total_customers,
            'total_products': total_products
        }
        return Response(data, status=status.HTTP_200_OK)
    

class LogoView(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]  # Only allow authenticated users

    def get_object(self):
        """
        Retrieve the first logo, assuming there is only one logo in the system.
        """
        return Logo.objects.first()

    def get(self, request, *args, **kwargs):
        """
        Retrieve the existing logo URL.
        """
        logo = self.get_object()  # Get the first logo instance
        if logo:
            serializer = self.get_serializer(logo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'No logo found.'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, *args, **kwargs):
        """
        Handles the creation of a new logo if one doesn't already exist.
        """
        if Logo.objects.exists():
            return Response({'detail': 'Logo already exists. Use PUT to update.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Update the existing logo.
        """
        logo = self.get_object()  # Fetch the existing logo
        if logo:
            serializer = self.get_serializer(logo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'No logo found to update.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        """
        Delete the existing logo.
        """
        logo = self.get_object()
        if logo:
            logo.delete()
            return Response({'detail': 'Logo deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'No logo found.'}, status=status.HTTP_404_NOT_FOUND)



class CustomerListView(generics.ListAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        # Filter only customers where is_customer is True
        return Customer.objects.filter(is_customer=True)

    def get(self, request, *args, **kwargs):
        customers = self.get_queryset()  # Fetch the customers with is_customer=True
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CustomerDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = CustomerSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs['id']
        try:
            customer = Customer.objects.get(id=customer_id, is_customer=True)
            products = Product.objects.filter(customer=customer)
            customer_data = CustomerSerializer(customer).data
            product_data = ProductSerializers(products, many=True).data

            return Response({
                'customer': customer_data,
                'products': product_data
            }, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        customer_id = self.kwargs['id']
        try:
            customer = Customer.objects.get(id=customer_id, is_customer=True)
            products = Product.objects.filter(customer=customer)
            
            # Delete all products first
            products.delete()

            # Delete the customer
            customer.delete()

            return Response({"message": "Customer and their products deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        

class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all categories."""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new category."""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Delete a category by ID."""
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
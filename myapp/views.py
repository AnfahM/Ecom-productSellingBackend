from rest_framework import generics, permissions ,status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from adminside.models import *
from adminside.serializers import *

Customer = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
                'customer':user.is_customer
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    

from rest_framework.response import Response
from rest_framework import status




class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Prepare product data
        product_data = {
            'name': request.data.get('name'),
            'price': request.data.get('price'),
            'phone_number': request.data.get('phone_number'),
            'description': request.data.get('description'),
            'customer': request.user.id,  # Set the customer from the authenticated user
            'category': request.data.get('category'),
        }

        # Create the product serializer
        product_serializer = ProductSerializer(data=product_data)

        if product_serializer.is_valid():
            # Save the product first to get a product instance
            product = product_serializer.save()

            # Handle the images from the request
            images = request.FILES.getlist('images')  # Get all uploaded images
            for image in images:
                product_image = ProductImage(image=image, product=product)
                product_image.save()  # Save each image instance

            # Handle the cover image if provided
            cover_image = request.FILES.get('cover_image')
            if cover_image:
                product.cover_image = cover_image
                product.save()  # Save the product again with the cover image

            return Response(product_serializer.data, status=status.HTTP_201_CREATED)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class MyProductsListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = []

    def get_queryset(self):
        # Only return products for the logged-in user
        return Product.objects.filter(customer=self.request.user)
    


from rest_framework.pagination import PageNumberPagination

# Custom pagination class
class ProductPagination(PageNumberPagination):
    page_size = 12  # Set initial page size to 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class AllProductsListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = []  # No permissions required
    pagination_class = ProductPagination  # Use the custom pagination

    def get_queryset(self):
        # Get optional 'category_id' from query parameters
        category_id = self.request.query_params.get('category', None)
        product_id = self.kwargs.get('id')  # Get optional 'id' from URL kwargs
        
        # Filter by product ID if provided in URL
        if product_id:
            return Product.objects.filter(id=product_id)
        
        # Filter by category if 'category_id' is provided in query parameters
        queryset = Product.objects.all()
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset


# views.py

class DeleteProductView(APIView):
    def delete(self, request, product_id, customer_id):
        try:
            product = Product.objects.get(id=product_id, customer_id=customer_id)
            product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

class ProductUpdateView(APIView):
    def put(self, request, product_id, customer_id):
        print("Received data:", request.data)  # Log the data for debugging
        try:
            product = Product.objects.get(id=product_id, customer_id=customer_id)
            serializer = ProductUpdateSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        







# View for retrieving, updating, and deleting a product
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Handle image upload if any new images are provided
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(image=image, product=product)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for uploading additional images for a product
class ProductImageUploadView(generics.CreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['product_id'])
        images = request.FILES.getlist('images')

        for image in images:
            ProductImage.objects.create(image=image, product=product)

        return Response({'message': 'Images uploaded successfully'}, status=status.HTTP_201_CREATED)

# View for deleting a specific product image
class ProductImageDeleteView(generics.DestroyAPIView):
    queryset = ProductImage.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        image = get_object_or_404(ProductImage, id=kwargs['image_id'])
        image.delete()
        return Response({'message': 'Image deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# View to set a specific image as the cover image
class ProductSetCoverImageView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['product_id'])
        image_id = request.data.get('image_id')  # Fetch the image ID from the request data

        if not image_id:
            return Response({'error': 'Image ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the image from the ProductImage model
        image = get_object_or_404(ProductImage, id=image_id, product=product)
        product.cover_image = image.image  # Set the cover image to the selected image
        product.save()

        return Response({'message': 'Cover image set successfully'}, status=status.HTTP_200_OK)



class LogoViewWithout(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer

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
    


class CategoryListViewCustomer(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
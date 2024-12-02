from django.urls import path
from .views import *
from adminside.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'), 
    path('sell/', ProductCreateView.as_view(), name='product-sell'),
    path('All-products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('my-products/', MyProductsListView.as_view(), name='my-products'),
    path('All-products/', AllProductsListView.as_view(), name='my-products'),
    path('All-products/<int:id>/', AllProductsListView.as_view(), name='product-detail'),
    path('categories/', CategoryListViewCustomer.as_view(), name='category-list'),
    path('my-products/<int:product_id>/<int:customer_id>/delete/', DeleteProductView.as_view(), name='delete-product'),
    path('my-products/<int:product_id>/<int:customer_id>/update/', ProductUpdateView.as_view(), name='update-product'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('products/<int:product_id>/upload-images/', ProductImageUploadView.as_view(), name='product-upload-images'),
    path('products/images/<int:image_id>/delete/', ProductImageDeleteView.as_view(), name='product-image-delete'),
    path('products/<int:product_id>/set-cover/', ProductSetCoverImageView.as_view(), name='product-set-cover-image'),
    path('logo/', LogoView.as_view(), name='logo'),
    path('logo/view/', LogoViewWithout.as_view(), name='logo'),
]

from myapp.models import *
from rest_framework import serializers
from .models import *

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = ['id', 'image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializers(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'phone_number', 'description', 'cover_image', 'product_images']

class CustomerSerializer(serializers.ModelSerializer):
    products = ProductSerializers(many=True, read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'email', 'username', 'phone_number', 'is_customer', 'products']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']
from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User
from .models import Order

#--------------------------Product Serializer---------------------
# Define your choices
CATEGORY_CHOICES = [
    ('electronics', 'Electronics'),
    ('fashion', 'Fashion'),
    ('home', 'Home & Kitchen'),
    ('beauty', 'Beauty & Health'),
    ('sports', 'Sports & Outdoor'),
    ('toys', 'Toys & Games'),
    ('automotive', 'Automotive'),
]

# Create ModelView Serializer 
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ['product_name','category','stock', 'quantity','quality','price','description','is_active','created_at','updated_at']


#--------------------------User Serializer---------------------
# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure that password is write-only
        }

    def create(self, validated_data):
        """Overriding the create method to handle password hashing"""
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Hashing the password
        user.save()
        return user

#--------------------------Order Serializer---------------------
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'price', 'delivery_time', 'status', 'created_at']
from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets, filters
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

#User Serializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

#cloudinary
import cloudinary.uploader



class HelloViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({"message": "Hello from API/n see other api baseurl/users,orders , products"})


#--------------product pagination-------------------
class ProductPagination(PageNumberPagination):
    page_size = 5  # Set custom page size
    page_size_query_param = 'page_size'
    max_page_size = 100

# class ProductViewSet(viewsets.ModelViewSet):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    # pagination_class = ProductPagination  # Use the custom pagination
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter,SearchFilter ]
    # filterset_fields = ['product_name', 'price']  # Specify the fields you want to allow filtering by
    # ordering_fields = ['product_name', 'price']
    # search_fields = ['product_name', 'price']  # fields you want to search in
    
    # # Optional: Customize response for creating a product
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         self.perform_create(serializer)
    #         return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # # Optional: Customize response for updating a product
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     if serializer.is_valid():
    #         self.perform_update(serializer)
    #         return Response({"message": "Product updated successfully"}, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # # Optional: Customize response for deleting a product
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['product_name', 'price']
    ordering_fields = ['product_name', 'price']
    search_fields = ['product_name', 'price']

    # Create a new product with Cloudinary image upload
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Handle image upload to Cloudinary
            image = request.FILES.get('image')
            if image:
                cloudinary_response = cloudinary.uploader.upload(image)
                cloudinary_url = cloudinary_response['secure_url']
                # Save Cloudinary URL in the serializer's validated data
                serializer.validated_data['image'] = cloudinary_url  # Now store the URL in the database

            self.perform_create(serializer)
            return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update a product with Cloudinary image upload
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            # Handle image upload to Cloudinary
            image = request.FILES.get('image')
            if image:
                cloudinary_response = cloudinary.uploader.upload(image)
                cloudinary_url = cloudinary_response['secure_url']
                # Update the Cloudinary URL in the instance
                instance.image = cloudinary_url

            self.perform_update(serializer)
            return Response({"message": "Product updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# -------------------- User Authentication Views using  ViewSet --------------------

class UserViewSet(viewsets.ViewSet):
    """
    A viewset for handling user authentication.
    """

    def create(self, request):
        """Handle user registration"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Handle user login"""
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response("Username and password are required", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response("Invalid credentials", status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response("Invalid credentials", status=status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], authentication_classes=[TokenAuthentication])
    def profile(self, request):
        """Get the authenticated user's profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


#------------------------Order View ------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return only orders for the currently authenticated user
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Optionally, set additional fields when creating an order (e.g., assign current user)
        serializer.save(user=self.request.user) 

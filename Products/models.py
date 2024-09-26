from django.db import models
from django.contrib.auth.models import User



class Product(models.Model):
    QUALITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home & Kitchen'),
        ('beauty', 'Beauty & Health'),
        ('sports', 'Sports & Outdoor'),
        ('toys', 'Toys & Games'),
        ('automotive', 'Automotive'),
        # Add more categories as needed
    ]

    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    stock = models.PositiveIntegerField()  # Number of items in stock
    quantity = models.PositiveIntegerField()  # Quantity for sale or per order
    quality = models.CharField(max_length=6, choices=QUALITY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price
    description = models.TextField(blank=True)  # Optional description
    is_active = models.BooleanField(default=True)  # Product availability
    created_at = models.DateTimeField(auto_now_add=True)  # Auto set at creation
    updated_at = models.DateTimeField(auto_now=True)  # Auto set at update
    image = models.ImageField(upload_to='temp/', blank=True, null=True)  # Temporary location for file
    
    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['-created_at']  # Order by newest products first


# ----------------------Order Model---------------------------
class Order(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
  
    class Meta:
        ordering = ['created_at']  # This will order orders by creation time

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

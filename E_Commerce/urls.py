from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

# from next_rest_api import views
from Products import views # type: ignore
#from .views import ProductListCreateView, ProductDetailView

from rest_framework.routers import DefaultRouter
# Create a router and register our viewset with it
router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='productslist')
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'orders', views.OrderViewSet, basename="orders")
router.register(r'', views.HelloViewSet, basename='hello')  # Base URL

urlpatterns = [
    path('admin/', admin.site.urls),
     path('api-auth/', include('rest_framework.urls')),
    # API endpoints for authentication and profile
    path('', include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

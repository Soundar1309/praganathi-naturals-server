"""
URL configuration for ecommerce project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Root API view
def api_root(request):
    return JsonResponse({
        "status": "OK",
        "message": "Pragathi Naturals API is running successfully!",
    })


# Root site view
def root_view(request):
    return JsonResponse({
        "status": "OK",
        "message": "Pragathi Naturals Backend is Running!",
    })


urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Health check endpoint
    path('up/', lambda request: HttpResponse('OK', status=200), name='health_check'),

    # API root (for CORS/debugging)
    path('api/', api_root, name='api_root'),

    # API routes (namespaced)
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/carts/', include('carts.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/wishlist/', include('wishlist.urls')),
    path('api/blogs/', include('blogs.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/admin/', include('admin_dashboard.urls')),

    # Root view for site
    path('', root_view, name='root'),
]

# Serve media/static in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

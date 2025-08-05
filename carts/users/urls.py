from django.urls import path
from . import views

urlpatterns = [
    # Authentication routes
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profile routes
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    
    # Address routes
    path('addresses/', views.AddressViewSet.as_view(), name='addresses'),
    path('addresses/<int:pk>/', views.AddressDetailView.as_view(), name='address_detail'),
] 
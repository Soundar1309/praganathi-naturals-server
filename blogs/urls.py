from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    # Public blog endpoints
    path('', views.BlogListView.as_view(), name='blog-list'),
    path('featured/', views.featured_blogs, name='featured-blogs'),
    path('categories/', views.BlogCategoryListView.as_view(), name='category-list'),
    path('tags/', views.BlogTagListView.as_view(), name='tag-list'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('<slug:slug>/related/', views.related_blogs, name='related-blogs'),
    path('<slug:slug>/comments/', views.BlogCommentCreateView.as_view(), name='blog-comments'),
    
    # Admin blog endpoints
    path('admin/create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('admin/<slug:slug>/update/', views.BlogUpdateView.as_view(), name='blog-update'),
    path('admin/<slug:slug>/delete/', views.BlogDeleteView.as_view(), name='blog-delete'),
]

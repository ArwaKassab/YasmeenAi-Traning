from django.urls import path
from . import views
from reviews.analytics_views import ProductAnalyticsView

urlpatterns = [
    path('', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:product_id>/analytics/', ProductAnalyticsView.as_view(), name='product-analytics'),
]
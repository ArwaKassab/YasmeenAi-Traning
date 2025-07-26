
from django.urls import path
from .analytics_views import (
    ReviewInteractionView, product_analytics, top_reviewers,
    top_rated_products, search_reviews_by_keywords
)

urlpatterns = [
    # تفاعل مع المراجعات
    path('<int:review_id>/like/', ReviewInteractionView.as_view(), name='review-interaction'),
    
    # تحليلات المنتجات
    path('analytics/products/<int:product_id>/', product_analytics, name='product-analytics'),
    path('analytics/top-reviewers/', top_reviewers, name='top-reviewers'),
    path('analytics/top-products/', top_rated_products, name='top-rated-products'),
    path('analytics/search/', search_reviews_by_keywords, name='search-reviews'),
]

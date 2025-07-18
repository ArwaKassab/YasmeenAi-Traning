from django.urls import path
from . import views
from .report_views import AdminReportView
from .analytics_views import ProductAnalyticsView, general_analytics, search_reviews_by_keywords
from .interaction_views import like_dislike_review, review_interactions_stats

urlpatterns = [
    # مراجعات عامة
    path('', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),

    # مراجعات منتج محدد
    path('product/<int:product_id>/', views.ProductReviewsView.as_view(), name='product-reviews'),
    path('product/<int:product_id>/summary/', views.product_rating_summary, name='product-rating-summary'),

    # إدارة المراجعات (للمدراء)
    path('<int:review_id>/approve/', views.approve_review, name='approve-review'),
    path('<int:review_id>/reject/', views.reject_review, name='reject-review'),
    path('pending/', views.pending_reviews, name='pending-reviews'),

    # تقارير المراجعات (للمدراء)
    path('admin/reports/', AdminReportView.as_view(), name='admin-reports'),

    # التحليلات
    path('analytics/general/', general_analytics, name='general-analytics'),
    path('analytics/search/', search_reviews_by_keywords, name='search-reviews'),

    # تفاعل المراجعات
    path('<int:review_id>/interact/', like_dislike_review, name='review-interact'),
    path('<int:review_id>/stats/', review_interactions_stats, name='review-stats'),
]
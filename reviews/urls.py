from django.urls import path, include
from . import views
from .report_views import AdminReportView,OffensiveReviewListView
urlpatterns = [
    # مراجعات عامة
    path('', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),

    # مراجعات منتج محدد
    path('product/<int:product_id>/', views.ProductReviewsView.as_view(),
         name='product-reviews'),
    path('product/<int:product_id>/summary/', views.product_rating_summary,
         name='product-rating-summary'),

    # إدارة المراجعات (للمدراء)
    path('<int:review_id>/approve/', views.approve_review, name='approve-review'),
    path('<int:review_id>/reject/', views.reject_review, name='reject-review'),
    path('pending/', views.pending_reviews, name='pending-reviews'),
   
    # تقارير المراجعات (للمدراء)
     path('admin/reports/', AdminReportView.as_view(), name='admin-reports'),
     path('admin/offensive-reviews/', OffensiveReviewListView.as_view(), name='offensive-reviews'),
     
     # تحليلات وتفاعل
     path('', include('reviews.analytics_urls')),

]
# review_reports/urls.py

from django.urls import path
from .views import (
    CreateReviewReportView,
    ReviewReportsForReviewView,
    AllReviewReportsView,
    HandleReviewReportView,
)

urlpatterns = [
    path('create/<int:review_id>/', CreateReviewReportView.as_view(), name='create-report'),
    path('<int:review_id>/', ReviewReportsForReviewView.as_view(), name='review-reports'),
    path('all/', AllReviewReportsView.as_view(), name='all-reports'),
    path('handle/<int:report_id>/', HandleReviewReportView.as_view(), name='handle-review-report'),
]

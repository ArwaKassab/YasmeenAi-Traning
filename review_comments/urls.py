from django.urls import path
from .views import ReviewCommentListCreateView

urlpatterns = [
     path('<int:review_id>/comments/', ReviewCommentListCreateView.as_view(), name='review-comments'),
]

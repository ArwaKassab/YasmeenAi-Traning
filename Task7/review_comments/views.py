# comments/views.py
from rest_framework import generics, permissions
from .models import ReviewComment
from .serializers import ReviewCommentSerializer
from notifications.realtime import notify_review_reply
from notifications.models import Notification
class ReviewCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return ReviewComment.objects.filter(review_id=review_id).order_by('created_at')

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        user=self.request.user
        comment = serializer.save(user=self.request.user, review_id=review_id)

        review = comment.review
        review_owner = review.user

        if review_owner != user:
            Notification.objects.create(
                user=review_owner,
                title="💬 رد على مراجعتك",
                message=f"{user.username} قام بالرد على مراجعتك: {comment.text}",
                review=review
            )

        notify_review_reply(comment)

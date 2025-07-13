from rest_framework import generics, permissions
from .models import ReviewComment
from .serializers import ReviewCommentSerializer
from notifications.realtime import notify_review_reply

class ReviewCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # جلب الردود للمراجعة المطلوبة
    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return ReviewComment.objects.filter(review_id=review_id).order_by('created_at')

    # إنشاء رد جديد
    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        comment = serializer.save(user=self.request.user, review_id=review_id)
        notify_review_reply(comment)  # إشعار لحظي لصاحب المراجعة

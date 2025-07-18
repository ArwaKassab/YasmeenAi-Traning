from rest_framework import generics, permissions
from .models import ReviewReport
from .serializers import ReviewReportSerializer
from reviews.models import Review
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminOnly
from notifications.models import Notification
from notifications.realtime import notify_user_deletion
from rest_framework.views import APIView


class CreateReviewReportView(generics.CreateAPIView):
    serializer_class = ReviewReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(user=self.request.user, review_id=review_id)

class ReviewReportsForReviewView(generics.ListAPIView):
    serializer_class = ReviewReportSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return ReviewReport.objects.filter(review_id=review_id)

class AllReviewReportsView(generics.ListAPIView):
    serializer_class = ReviewReportSerializer
    permission_classes = [IsAdminOnly]
    queryset = ReviewReport.objects.select_related('review', 'user').all()


class HandleReviewReportView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOnly]

    def post(self, request, *args, **kwargs):
        report_id = kwargs.get('report_id')
        try:
            report = ReviewReport.objects.select_related('review__user', 'review__product').get(id=report_id)
            review = report.review

            review_owner = review.user
            product_name = review.product.name
            review_id = review.id
            review_text = review.text

            review.approval_status = 'rejected'
            review.save()

            Notification.objects.create(
                user=review_owner,
                title="🚫 تم رفض مراجعتك",
                message=f"تم رفض مراجعتك عن المنتج: {product_name} بعد مراجعة البلاغ.",
                review=review
            )

            # إشعار لحظي بالرفض
            notify_user_deletion({
                "user_id": review_owner.id,
                "product_name": product_name,
                "review_id": review_id,
                "review_text": review_text
            })

            return Response({"detail": "تم رفض المراجعة وإرسال الإشعار."}, status=status.HTTP_200_OK)

        except ReviewReport.DoesNotExist:
            return Response({"detail": "البلاغ غير موجود."}, status=status.HTTP_404_NOT_FOUND)


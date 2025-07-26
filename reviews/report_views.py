from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly
from .models import Review
from .serializers import ReviewSerializer
from rest_framework import  permissions

BANNED_WORDS = ['stupid', 'غبي', 'أنتم نصابين', 'المنتج نصب', 'حرامية' ]

class AdminReportView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        pending_qs = Review.objects.filter(approval_status='pending')
        rejected_or_low_qs = Review.objects.filter(approval_status='rejected') | Review.objects.filter(rating__lte=2)
        offensive_qs = Review.objects.filter(
            text__iregex=r'(' + '|'.join(BANNED_WORDS) + ')'
        )

        return Response({
            'pending_reviews_count': pending_qs.count(),
            'pending_reviews': ReviewSerializer(pending_qs, many=True).data,

            'rejected_or_low_reviews_count': rejected_or_low_qs.count(),
            'rejected_or_low_reviews': ReviewSerializer(rejected_or_low_qs, many=True).data,

            'offensive_reviews_count': offensive_qs.count(),
            'offensive_reviews': ReviewSerializer(offensive_qs, many=True).data,
        })


class OffensiveReviewListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        banned_pattern = r'(' + '|'.join(BANNED_WORDS) + ')'
        offensive_reviews = Review.objects.filter(text__iregex=banned_pattern)
        serializer = ReviewSerializer(offensive_reviews, many=True)
        return Response({
            'count': offensive_reviews.count(),
            'offensive_reviews': serializer.data
        })
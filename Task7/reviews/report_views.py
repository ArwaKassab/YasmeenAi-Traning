# reviews/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .models import Review

BANNED_WORDS = ['stupid', 'غبي', 'أنتم نصابين', 'المنتج نصب', 'حرامية' ]

class AdminReportView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        pending = Review.objects.filter(approval_status='pending').count()
        rejected_or_low = (
            Review.objects.filter(approval_status='rejected').count() +
            Review.objects.filter(rating__lte=2).count()
        )
        offensive = Review.objects.filter(
            text__iregex=r'(' + '|'.join(BANNED_WORDS) + ')'
        ).count()

        return Response({
            'pending_reviews': pending,
            'rejected_or_low_reviews': rejected_or_low,
            'offensive_reviews': offensive
        })

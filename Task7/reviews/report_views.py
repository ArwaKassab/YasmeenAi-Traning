# reviews/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Review

BANNED_WORDS = ['كلمة1', 'كلمة2', 'كلمة3']  # قائمة كلمات مسيئة

class AdminReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        pending = Review.objects.filter(status='pending').count()
        rejected_or_low = Review.objects.filter(status='rejected').count() + Review.objects.filter(rating__lte=2).count()
        offensive = Review.objects.filter(content__iregex=r'(' + '|'.join(BANNED_WORDS) + ')').count()

        return Response({
            'pending_reviews': pending,
            'rejected_or_low_reviews': rejected_or_low,
            'offensive_reviews': offensive
        })

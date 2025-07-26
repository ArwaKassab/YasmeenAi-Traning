# review_reports/models.py

from django.db import models
from django.conf import settings
from reviews.models import Review

class ReviewReport(models.Model):
    REASON_CHOICES = [
        ('offensive', 'محتوى مسيء'),
        ('incorrect', 'المراجعة غير صحيحة'),
        ('other', 'غير ذلك'),
    ]

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    note = models.TextField(blank=True, null=True, verbose_name="ملاحظة إضافية")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')  # يمنع تكرار الإبلاغ

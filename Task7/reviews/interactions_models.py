
from django.db import models
from django.conf import settings
from .models import Review


class ReviewInteraction(models.Model):
    INTERACTION_CHOICES = [
        ('helpful', 'مفيدة'),
        ('not_helpful', 'غير مفيدة'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review_interactions',
        verbose_name="المستخدم"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='interactions',
        verbose_name="المراجعة"
    )
    interaction_type = models.CharField(
        max_length=15,
        choices=INTERACTION_CHOICES,
        verbose_name="نوع التفاعل"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'review')
        verbose_name = "تفاعل مع المراجعة"
        verbose_name_plural = "التفاعلات مع المراجعات"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_interaction_type_display()} - {self.review.id}"

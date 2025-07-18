from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from reviews.models import Review 

class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_comments')
    text = models.TextField(verbose_name="الرد")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"رد من {self.user.username} على مراجعة {self.review.id}"

from django.db import models
from django.contrib.auth import get_user_model
from reviews.models import Review 

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    review = models.ForeignKey(Review, null=True, blank=True, on_delete=models.SET_NULL) 
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.user.username} - {self.title}"

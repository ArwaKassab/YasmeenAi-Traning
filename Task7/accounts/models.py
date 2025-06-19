from django.contrib.auth.models import AbstractUser
from django.db import models

def user_profile_image_path(instance, filename):
    return f'user_{instance.id}/{filename}'

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'أدمن'),
        ('user', 'مستخدم عادي'),

    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False)
    profile_image = models.ImageField(upload_to=user_profile_image_path, null=True, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.email}) - {self.get_role_display()}"

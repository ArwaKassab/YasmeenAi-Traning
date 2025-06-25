from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product


class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} نجوم") for i in range(1, 6)]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="المنتج"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="المستخدم"
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="التقييم"
    )
    text = models.TextField(verbose_name="نص المراجعة")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False, verbose_name="معتمدة")

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')  # مستخدم واحد لكل منتج
        verbose_name = "مراجعة"
        verbose_name_plural = "المراجعات"

    def __str__(self):
        return f"مراجعة {self.user.username} لـ {self.product.name}"
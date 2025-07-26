# products/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المنتج")
    description = models.TextField(verbose_name="وصف المنتج")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        verbose_name="السعر"
    )
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        """حساب متوسط التقييم للمراجعات المعتمدة"""
        approved_reviews = self.reviews.filter(approval_status='approved')
        if approved_reviews.exists():
            return round(approved_reviews.aggregate(
                models.Avg('rating')
            )['rating__avg'], 2)
        return 0

    @property
    def reviews_count(self):
        """عدد المراجعات المعتمدة"""
        return self.reviews.filter(approval_status='approved').count()
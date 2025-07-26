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
    views = models.PositiveIntegerField(default=0, verbose_name="عدد المشاهدات") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    APPROVAL_CHOICES = [
        ('pending', 'معلق'),
        ('approved', 'مقبول'),
        ('rejected', 'مرفوض'),
    ]

    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default='pending',
        verbose_name="حالة الموافقة"
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')  
        verbose_name = "مراجعة"
        verbose_name_plural = "المراجعات"

    def __str__(self):
        return f"مراجعة {self.user.username} لـ {self.product.name}"
    
    @property
    def helpful_count(self):
        """عدد التفاعلات المفيدة"""
        return self.interactions.filter(interaction_type='helpful').count()
    
    @property
    def not_helpful_count(self):
        """عدد التفاعلات غير المفيدة"""
        return self.interactions.filter(interaction_type='not_helpful').count()
    
    @property
    def total_interactions(self):
        """إجمالي التفاعلات"""
        return self.interactions.count()
    
    @property
    def helpfulness_score(self):
        """درجة الفائدة (للترتيب)"""
        helpful = self.helpful_count
        total = self.total_interactions
        if total == 0:
            return 0
        return (helpful / total) * 100
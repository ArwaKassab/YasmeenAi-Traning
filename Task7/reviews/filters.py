
import django_filters
from django.db.models import Q, Count
from .models import Review


class ReviewFilter(django_filters.FilterSet):
    """
    فلتر مخصص للمراجعات مع دعم التصفية المتقدمة
    """
    # تصفية حسب التقييم
    rating = django_filters.NumberFilter(field_name='rating')
    rating_min = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_max = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')
    
    # تصفية حسب المنتج
    product = django_filters.NumberFilter(field_name='product')
    product_name = django_filters.CharFilter(field_name='product__name', lookup_expr='icontains')
    
    # تصفية حسب حالة الموافقة
    approval_status = django_filters.ChoiceFilter(choices=Review.APPROVAL_CHOICES)
    
    # تصفية حسب التاريخ
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    
    # تصفية حسب عدد المشاهدات
    min_views = django_filters.NumberFilter(field_name='views', lookup_expr='gte')
    max_views = django_filters.NumberFilter(field_name='views', lookup_expr='lte')
    
    # تصفية حسب وجود تفاعلات
    has_interactions = django_filters.BooleanFilter(method='filter_has_interactions')
    
    # تصفية حسب المستخدم
    user = django_filters.NumberFilter(field_name='user')
    user_name = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    
    # تصفية المراجعات عالية التقييم (4 و 5 نجوم)
    high_rating_only = django_filters.BooleanFilter(method='filter_high_rating')
    
    # تصفية المراجعات منخفضة التقييم (1 و 2 نجمة)
    low_rating_only = django_filters.BooleanFilter(method='filter_low_rating')

    class Meta:
        model = Review
        fields = [
            'rating', 'rating_min', 'rating_max',
            'product', 'product_name',
            'approval_status',
            'date_from', 'date_to',
            'min_views', 'max_views',
            'has_interactions',
            'user', 'user_name',
            'high_rating_only', 'low_rating_only'
        ]

    def filter_has_interactions(self, queryset, name, value):
        """تصفية المراجعات التي لديها تفاعلات"""
        if value:
            return queryset.annotate(
                interactions_count=Count('interactions')
            ).filter(interactions_count__gt=0)
        return queryset

    def filter_high_rating(self, queryset, name, value):
        """تصفية المراجعات عالية التقييم (4-5 نجوم)"""
        if value:
            return queryset.filter(rating__gte=4)
        return queryset

    def filter_low_rating(self, queryset, name, value):
        """تصفية المراجعات منخفضة التقييم (1-2 نجمة)"""
        if value:
            return queryset.filter(rating__lte=2)
        return queryset

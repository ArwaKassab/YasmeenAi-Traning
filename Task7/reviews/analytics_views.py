from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Avg, Q, F
from django.utils import timezone
from datetime import timedelta
from .models import Review
from .interactions_models import ReviewInteraction
from products.models import Product
from accounts.models import User
from .interactions_serializers import (
    ReviewInteractionSerializer, ProductAnalyticsSerializer,
    TopReviewersSerializer, KeywordSearchSerializer
)


class ReviewInteractionView(generics.CreateAPIView):
    """
    تفاعل المستخدم مع المراجعة (مفيدة/غير مفيدة)
    """
    serializer_class = ReviewInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        review_id = self.kwargs['review_id']

        try:
            review = Review.objects.get(id=review_id, approval_status='approved')
        except Review.DoesNotExist:
            return Response(
                {"error": "المراجعة غير موجودة أو غير معتمدة"},
                status=status.HTTP_404_NOT_FOUND
            )
        # التحقق من وجود تفاعل سابق وتحديثه أو إنشاء جديد
        interaction, created = ReviewInteraction.objects.update_or_create(
            user=request.user,
            review=review,
            defaults={'interaction_type': request.data.get('interaction_type')}
        )

        serializer = self.get_serializer(interaction)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        message = "تم تسجيل تفاعلك" if created else "تم تحديث تفاعلك"

        return Response({
            "message": message,
            "interaction": serializer.data,
            "helpful_count": review.helpful_count,
            "not_helpful_count": review.not_helpful_count
        }, status=status_code)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_analytics(request, product_id):
    """
    تحليلات التقييمات لمنتج محدد
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "المنتج غير موجود"},
            status=status.HTTP_404_NOT_FOUND
        )

    # الحصول على الفترة الزمنية (افتراضياً 30 يوم)
    days = int(request.query_params.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)

    # الحصول على جميع المراجعات المعتمدة للمنتج
    all_reviews = Review.objects.filter(product=product, approval_status='approved')
    period_reviews = all_reviews.filter(created_at__gte=start_date)

    # حساب الإحصائيات العامة
    total_reviews = all_reviews.count()
    average_rating = all_reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # حساب إحصائيات الفترة المحددة
    period_reviews_count = period_reviews.count()
    period_average_rating = period_reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # توزيع التقييمات
    rating_distribution = {}
    for i in range(1, 6):
        rating_distribution[f'{i}_stars'] = period_reviews.filter(rating=i).count()
    # أفضل مراجعة بناءً على التفاعل
    top_review = all_reviews.annotate(
        helpful_count=Count('interactions', filter=Q(interactions__interaction_type='helpful')),
        total_interactions=Count('interactions')
    ).filter(total_interactions__gt=0).order_by('-helpful_count', '-total_interactions').first()
    analytics_data = {
        'product_id': product.id,
        'product_name': product.name,
        'total_reviews': total_reviews,
        'average_rating': round(average_rating, 2),
        'period_reviews': period_reviews_count,
        'period_average_rating': round(period_average_rating, 2),
        'rating_distribution': rating_distribution,
        'top_review': top_review,
        'period_days': days
    }
    serializer = ProductAnalyticsSerializer(analytics_data, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def top_reviewers(request):
    """
    أكثر المستخدمين كتابةً للمراجعات
    """
    if request.user.role != 'admin':
        return Response(
            {"error": "ليس لديك صلاحية للوصول لهذه الخدمة"},
            status=status.HTTP_403_FORBIDDEN
        )

    # الحصول على الفترة الزمنية (افتراضياً 30 يوم)
    days = int(request.query_params.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)

    top_reviewers = User.objects.filter(
        reviews__approval_status='approved',
        reviews__created_at__gte=start_date
    ).annotate(
        reviews_count=Count('reviews'),
        average_rating_given=Avg('reviews__rating')
    ).filter(reviews_count__gt=0).order_by('-reviews_count')[:10]
    data = []
    for user in top_reviewers:
        data.append({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'reviews_count': user.reviews_count,
            'average_rating_given': round(user.average_rating_given, 2)
        })
    serializer = TopReviewersSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def top_rated_products(request):
    """
    المنتجات التي حصلت على أعلى تقييم خلال الفترة الأخيرة
    """
    days = int(request.query_params.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    products = Product.objects.filter(
        reviews__approval_status='approved',
        reviews__created_at__gte=start_date
    ).annotate(
        period_reviews_count=Count('reviews'),
        period_average_rating=Avg('reviews__rating')
    ).filter(
        period_reviews_count__gte=3  # على الأقل 3 مراجعات
    ).order_by('-period_average_rating')[:10]
    data = []
    for product in products:
        data.append({
            'product_id': product.id,
            'product_name': product.name,
            'period_reviews_count': product.period_reviews_count,
            'period_average_rating': round(product.period_average_rating, 2)
        })
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_reviews_by_keywords(request):
    """
    البحث في المراجعات بالكلمات المفتاحية
    """
    keyword = request.query_params.get('keyword', '').strip()
    if not keyword:
        return Response(
            {"error": "يجب تحديد كلمة مفتاحية للبحث"},
            status=status.HTTP_400_BAD_REQUEST
        )
    reviews = Review.objects.filter(
        Q(text__icontains=keyword),
        approval_status='approved'
    ).select_related('user', 'product').order_by('-created_at')
    data = {
        'keyword': keyword,
        'reviews': reviews
    }

    serializer = KeywordSearchSerializer(data, context={'request': request})
    return Response(serializer.data)

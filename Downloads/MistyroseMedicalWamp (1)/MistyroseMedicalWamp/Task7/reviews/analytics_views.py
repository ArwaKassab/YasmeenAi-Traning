
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg, Count, Case, When, IntegerField
from django.utils import timezone
from datetime import timedelta
from .models import Review
from .interaction_models import ReviewInteraction
from products.models import Product
from accounts.models import User


class ProductAnalyticsView(generics.RetrieveAPIView):
    """
    تحليلات المنتج - معدل التقييم والإحصائيات
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "المنتج غير موجود"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # الحصول على فترة زمنية (افتراضي 30 يوم)
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # المراجعات المعتمدة في الفترة المحددة
        reviews_in_period = Review.objects.filter(
            product=product,
            approval_status='approved',
            created_at__gte=start_date
        )
        
        # معدل التقييم في الفترة
        avg_rating = reviews_in_period.aggregate(
            avg=Avg('rating')
        )['avg'] or 0
        
        # عدد المراجعات في الفترة
        reviews_count = reviews_in_period.count()
        
        # توزيع التقييمات
        rating_distribution = {}
        for i in range(1, 6):
            count = reviews_in_period.filter(rating=i).count()
            rating_distribution[f"{i}_stars"] = count
        
        # أفضل مراجعة بناءً على التفاعل
        top_review = reviews_in_period.annotate(
            likes_count=Count(
                Case(
                    When(interactions__interaction_type='like', then=1),
                    output_field=IntegerField()
                )
            ),
            dislikes_count=Count(
                Case(
                    When(interactions__interaction_type='dislike', then=1),
                    output_field=IntegerField()
                )
            ),
            score=Count(
                Case(
                    When(interactions__interaction_type='like', then=1),
                    output_field=IntegerField()
                )
            ) - Count(
                Case(
                    When(interactions__interaction_type='dislike', then=1),
                    output_field=IntegerField()
                )
            )
        ).order_by('-score', '-created_at').first()
        
        top_review_data = None
        if top_review:
            top_review_data = {
                'id': top_review.id,
                'user': top_review.user.username,
                'rating': top_review.rating,
                'text': top_review.text,
                'likes': top_review.likes_count,
                'dislikes': top_review.dislikes_count,
                'score': top_review.score,
                'created_at': top_review.created_at
            }
        
        data = {
            'product': {
                'id': product.id,
                'name': product.name
            },
            'period_days': days,
            'average_rating': round(avg_rating, 2),
            'reviews_count': reviews_count,
            'rating_distribution': rating_distribution,
            'top_review': top_review_data
        }
        
        return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def general_analytics(request):
    """
    تحليلات عامة للنظام
    """
    if request.user.role != 'admin':
        return Response(
            {"error": "ليس لديك صلاحية للوصول لهذه الخدمة"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    days = int(request.query_params.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # أكثر المستخدمين كتابة للمراجعات
    top_reviewers = User.objects.annotate(
        reviews_count=Count(
            'reviews',
            filter=Q(
                reviews__created_at__gte=start_date,
                reviews__approval_status='approved'
            )
        )
    ).filter(reviews_count__gt=0).order_by('-reviews_count')[:10]
    
    top_reviewers_data = [
        {
            'user': user.username,
            'email': user.email,
            'reviews_count': user.reviews_count
        }
        for user in top_reviewers
    ]
    
    # المنتجات التي حصلت على أعلى تقييم
    top_rated_products = Product.objects.annotate(
        avg_rating=Avg(
            'reviews__rating',
            filter=Q(
                reviews__created_at__gte=start_date,
                reviews__approval_status='approved'
            )
        ),
        period_reviews_count=Count(
            'reviews',
            filter=Q(
                reviews__created_at__gte=start_date,
                reviews__approval_status='approved'
            )
        )
    ).filter(
        period_reviews_count__gt=0
    ).order_by('-avg_rating', '-period_reviews_count')[:10]
    
    top_products_data = [
        {
            'id': product.id,
            'name': product.name,
            'average_rating': round(product.avg_rating or 0, 2),
            'reviews_count': product.period_reviews_count
        }
        for product in top_rated_products
    ]
    
    data = {
        'period_days': days,
        'top_reviewers': top_reviewers_data,
        'top_rated_products': top_products_data
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_reviews_by_keywords(request):
    """
    البحث في المراجعات بالكلمات المفتاحية
    """
    keywords = request.query_params.get('keywords', '')
    if not keywords:
        return Response(
            {"error": "يجب توفير كلمات مفتاحية للبحث"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # البحث في نص المراجعات
    reviews = Review.objects.filter(
        text__icontains=keywords,
        approval_status='approved'
    ).select_related('user', 'product').order_by('-created_at')
    
    results = []
    for review in reviews:
        results.append({
            'id': review.id,
            'product': {
                'id': review.product.id,
                'name': review.product.name
            },
            'user': review.user.username,
            'rating': review.rating,
            'text': review.text,
            'created_at': review.created_at
        })
    
    return Response({
        'keywords': keywords,
        'results_count': len(results),
        'reviews': results
    })

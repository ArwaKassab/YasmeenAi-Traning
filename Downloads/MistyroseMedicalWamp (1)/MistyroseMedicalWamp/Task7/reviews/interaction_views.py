
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Case, When, IntegerField
from .models import Review
from .interaction_models import ReviewInteraction


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_dislike_review(request, review_id):
    """
    تقييم المراجعة بأنها مفيدة أو غير مفيدة
    """
    try:
        review = Review.objects.get(id=review_id, approval_status='approved')
    except Review.DoesNotExist:
        return Response(
            {"error": "المراجعة غير موجودة أو غير معتمدة"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # منع المستخدم من تقييم مراجعته الخاصة
    if review.user == request.user:
        return Response(
            {"error": "لا يمكنك تقييم مراجعتك الخاصة"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    interaction_type = request.data.get('type')
    if interaction_type not in ['like', 'dislike']:
        return Response(
            {"error": "نوع التفاعل يجب أن يكون 'like' أو 'dislike'"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # البحث عن تفاعل سابق
    interaction, created = ReviewInteraction.objects.get_or_create(
        user=request.user,
        review=review,
        defaults={'interaction_type': interaction_type}
    )
    
    if not created:
        if interaction.interaction_type == interaction_type:
            # إلغاء التفاعل إذا كان نفس النوع
            interaction.delete()
            message = "تم إلغاء التفاعل"
        else:
            # تغيير نوع التفاعل
            interaction.interaction_type = interaction_type
            interaction.save()
            message = f"تم تغيير التفاعل إلى {interaction.get_interaction_type_display()}"
    else:
        message = f"تم إضافة تفاعل: {interaction.get_interaction_type_display()}"
    
    # حساب الإحصائيات الحديثة
    stats = ReviewInteraction.objects.filter(review=review).aggregate(
        likes=Count(
            Case(
                When(interaction_type='like', then=1),
                output_field=IntegerField()
            )
        ),
        dislikes=Count(
            Case(
                When(interaction_type='dislike', then=1),
                output_field=IntegerField()
            )
        )
    )
    
    return Response({
        'message': message,
        'review_id': review.id,
        'likes': stats['likes'],
        'dislikes': stats['dislikes'],
        'score': stats['likes'] - stats['dislikes']
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def review_interactions_stats(request, review_id):
    """
    إحصائيات تفاعل المراجعة
    """
    try:
        review = Review.objects.get(id=review_id, approval_status='approved')
    except Review.DoesNotExist:
        return Response(
            {"error": "المراجعة غير موجودة أو غير معتمدة"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    stats = ReviewInteraction.objects.filter(review=review).aggregate(
        likes=Count(
            Case(
                When(interaction_type='like', then=1),
                output_field=IntegerField()
            )
        ),
        dislikes=Count(
            Case(
                When(interaction_type='dislike', then=1),
                output_field=IntegerField()
            )
        )
    )
    
    user_interaction = None
    if request.user.is_authenticated:
        try:
            interaction = ReviewInteraction.objects.get(
                user=request.user,
                review=review
            )
            user_interaction = interaction.interaction_type
        except ReviewInteraction.DoesNotExist:
            pass
    
    return Response({
        'review_id': review.id,
        'likes': stats['likes'],
        'dislikes': stats['dislikes'],
        'score': stats['likes'] - stats['dislikes'],
        'user_interaction': user_interaction
    })


from rest_framework import serializers
from .interactions_models import ReviewInteraction
from .models import Review
from products.models import Product
from accounts.models import User
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta


class ReviewInteractionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ReviewInteraction
        fields = ['id', 'user', 'user_name', 'review', 'interaction_type', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            review = attrs.get('review')
            
            # منع المستخدم من التفاعل مع مراجعته الخاصة
            if review.user == user:
                raise serializers.ValidationError("لا يمكنك التفاعل مع مراجعتك الخاصة")
        
        return attrs


class ProductAnalyticsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    
    # إحصائيات عامة
    total_reviews = serializers.IntegerField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    
    # إحصائيات الفترة المحددة
    period_reviews = serializers.IntegerField()
    period_average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    
    # توزيع التقييمات
    rating_distribution = serializers.DictField()
    
    # أفضل مراجعة
    top_review = serializers.SerializerMethodField()
    
    def get_top_review(self, obj):
        from .serializers import ReviewSerializer
        top_review = obj.get('top_review')
        if top_review:
            return ReviewSerializer(top_review, context=self.context).data
        return None


class TopReviewersSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    reviews_count = serializers.IntegerField()
    average_rating_given = serializers.DecimalField(max_digits=3, decimal_places=2)


class KeywordSearchSerializer(serializers.Serializer):
    keyword = serializers.CharField()
    reviews = serializers.SerializerMethodField()
    
    def get_reviews(self, obj):
        from .serializers import ReviewSerializer
        return ReviewSerializer(obj['reviews'], many=True, context=self.context).data

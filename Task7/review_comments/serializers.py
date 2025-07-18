# comments/serializers.py
from rest_framework import serializers
from .models import ReviewComment

class ReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # للعرض فقط

    class Meta:
        model = ReviewComment
        fields = ['id', 'review', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'created_at', 'review']

    def create(self, validated_data):
        request = self.context.get('request')
        review_id = self.context['view'].kwargs.get('review_id')
        return ReviewComment.objects.create(
            user=request.user,
            review_id=review_id,
            **validated_data
        )

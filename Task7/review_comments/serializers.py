from rest_framework import serializers
from .models import ReviewComment

class ReviewCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ReviewComment
        fields = ['id', 'review', 'user', 'user_name', 'text',]
        read_only_fields = ['user', 'review', 'created_at']

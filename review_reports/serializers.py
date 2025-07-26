from rest_framework import serializers
from .models import ReviewReport

class ReviewReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReport
        fields = ['id', 'review', 'user', 'reason', 'note', 'created_at']
        read_only_fields = ['user', 'created_at']
        extra_kwargs = {
            'review': {'required': False}  
        }

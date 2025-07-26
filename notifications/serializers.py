from rest_framework import serializers
from notifications.models import Notification
from review_reports.models import ReviewReport

class NotificationSerializer(serializers.ModelSerializer):
    review_id = serializers.SerializerMethodField()
    review_text = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at', 'review_id', 'review_text']

    def get_review_id(self, obj):
        try:
            return obj.review.id
        except AttributeError:
            return None

    def get_review_text(self, obj):
        try:
            return obj.review.text
        except AttributeError:
            return None

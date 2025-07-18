from rest_framework import serializers
from .models import Review
from products.models import Product
from review_comments.serializers import ReviewCommentSerializer


class ReviewReportFieldsMixin:
    has_report = serializers.SerializerMethodField()
    report_id = serializers.SerializerMethodField()

    def _get_report_info(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'admin':
            report = obj.reports.first()
            if report:
                return {"has_report": True, "report_id": report.id}
        return {"has_report": False, "report_id": None}

    def get_has_report(self, obj):
        return self._get_report_info(obj)['has_report']

    def get_report_id(self, obj):
        return self._get_report_info(obj)['report_id']


class ReviewSerializer(ReviewReportFieldsMixin, serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    comments_count = serializers.SerializerMethodField()
    has_report = serializers.SerializerMethodField()
    report_id = serializers.SerializerMethodField()


    class Meta:
        model = Review
        fields = [
            'id', 'product', 'user', 'user_name', 'product_name',
            'rating', 'text', 'created_at', 'updated_at', 'approval_status',
            'comments_count', 'views', 'has_report', 'report_id'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("التقييم يجب أن يكون بين 1 و 5")
        return value

    def validate_product(self, value):
        if not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("المنتج غير موجود")
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            product = attrs.get('product')
            if not self.instance:
                if Review.objects.filter(user=user, product=product).exists():
                    raise serializers.ValidationError("لقد قمت بمراجعة هذا المنتج من قبل")
        return attrs


class ReviewCreateSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        fields = ['product', 'rating', 'text']


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'text']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("التقييم يجب أن يكون بين 1 و 5")
        return value


class ProductRatingSummarySerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()
    reviews_count = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'average_rating', 'reviews_count']


class ReviewDetailSerializer(ReviewReportFieldsMixin, serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    comments = ReviewCommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    has_report = serializers.SerializerMethodField()
    report_id = serializers.SerializerMethodField()


    class Meta:
        model = Review
        fields = [
            'id', 'product', 'user', 'user_name', 'product_name',
            'rating', 'text', 'created_at', 'updated_at',
            'approval_status', 'views', 'comments',
            'comments_count', 'has_report', 'report_id'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_comments_count(self, obj):
        return obj.comments.count()

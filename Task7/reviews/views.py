from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Review
from products.models import Product
from .serializers import (
    ReviewSerializer, ReviewCreateSerializer,
    ReviewUpdateSerializer, ProductRatingSummarySerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    عرض قائمة المراجعات وإنشاء مراجعة جديدة
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['rating', 'product', 'is_approved']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    search_fields = ['text', 'product__name']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Review.objects.all()
        else:
            # المستخدمون العاديون يرون المراجعات المعتمدة فقط + مراجعاتهم الخاصة
            return Review.objects.filter(
                Q(is_approved=True) | Q(user=user)
            )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    عرض، تحديث، أو حذف مراجعة محددة
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Review.objects.all()
        else:
            return Review.objects.filter(
                Q(is_approved=True) | Q(user=user)
            )

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReviewUpdateSerializer
        return ReviewSerializer


class ProductReviewsView(generics.ListAPIView):
    """
    عرض مراجعات منتج معين
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(
            product_id=product_id,
            is_approved=True
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_rating_summary(request, product_id):
    """
    الحصول على ملخص تقييم المنتج
    """
    try:
        product = Product.objects.get(id=product_id)
        serializer = ProductRatingSummarySerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(
            {"error": "المنتج غير موجود"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_review(request, review_id):
    """
    الموافقة على مراجعة (للمدراء فقط)
    """
    if request.user.role != 'admin':
        return Response(
            {"error": "ليس لديك صلاحية للوصول لهذه الخدمة"},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        review = Review.objects.get(id=review_id)
        review.is_approved = True
        review.save()
        return Response(
            {"message": "تم اعتماد المراجعة بنجاح"},
            status=status.HTTP_200_OK
        )
    except Review.DoesNotExist:
        return Response(
            {"error": "المراجعة غير موجودة"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_review(request, review_id):
    """
    رفض مراجعة (للمدراء فقط)
    """
    if request.user.role != 'admin':
        return Response(
            {"error": "ليس لديك صلاحية للوصول لهذه الخدمة"},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        review = Review.objects.get(id=review_id)
        review.is_approved = False
        review.save()
        return Response(
            {"message": "تم رفض المراجعة"},
            status=status.HTTP_200_OK
        )
    except Review.DoesNotExist:
        return Response(
            {"error": "المراجعة غير موجودة"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_reviews(request):
    """
    عرض المراجعات في انتظار الموافقة (للمدراء فقط)
    """
    if request.user.role != 'admin':
        return Response(
            {"error": "ليس لديك صلاحية للوصول لهذه الخدمة"},
            status=status.HTTP_403_FORBIDDEN
        )

    reviews = Review.objects.filter(is_approved=False)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

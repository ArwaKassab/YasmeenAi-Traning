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
    ,ReviewDetailSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from notifications.realtime import notify_user
from django.db import models


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    عرض قائمة المراجعات وإنشاء مراجعة جديدة
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['rating', 'product', 'approval_status']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    search_fields = ['text', 'product__name']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Review.objects.all()
        else:
            return Review.objects.filter(
                Q(approval_status='approved') | Q(user=user)
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
                Q(approval_status='approved') | Q(user=user)
            )

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReviewUpdateSerializer
        return ReviewDetailSerializer
    
        """
    حساب عدد المشاهدات
    """
    def get_object(self):
        obj = super().get_object()

        obj.views = models.F('views') + 1  
        obj.save(update_fields=["views"]) 

        obj.refresh_from_db() 
        return obj


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
            approval_status='approved'
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
        review.approval_status = 'approved'
        review.save()
        notify_user(review)
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
        review.approval_status = 'rejected'
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

    reviews = Review.objects.filter(approval_status='pending')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

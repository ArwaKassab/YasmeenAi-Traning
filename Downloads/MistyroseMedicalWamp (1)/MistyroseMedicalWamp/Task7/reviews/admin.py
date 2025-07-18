from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'approval_status', 'created_at']
    list_filter = ['rating', 'approval_status', 'created_at']
    search_fields = ['user__username', 'product__name', 'text']
    actions = ['approve_reviews', 'reject_reviews', 'mark_pending']

    def approve_reviews(self, request, queryset):
        updated = queryset.update(approval_status='approved')
        self.message_user(request, f'{updated} مراجعة تم اعتمادها.')

    approve_reviews.short_description = 'اعتماد المراجعات المحددة'

    def reject_reviews(self, request, queryset):
        updated = queryset.update(approval_status='rejected')
        self.message_user(request, f'{updated} مراجعة تم رفضها.')

    reject_reviews.short_description = 'رفض المراجعات المحددة'

    def mark_pending(self, request, queryset):
        updated = queryset.update(approval_status='pending')
        self.message_user(request, f'{updated} مراجعة تم وضعها كمعلقة.')

    mark_pending.short_description = 'تعيين المراجعات كمعلقة'

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ReviewComment

@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'created_at']
    search_fields = ['text', 'user__username']

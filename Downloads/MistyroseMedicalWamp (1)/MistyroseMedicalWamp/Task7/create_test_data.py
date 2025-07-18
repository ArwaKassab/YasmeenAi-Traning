
#!/usr/bin/env python
import os
import sys
import django

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# تحديد إعدادات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_reviews.settings')

# إعداد Django
django.setup()

# الآن يمكن استيراد النماذج
from accounts.models import User
from products.models import Product
from reviews.models import Review
from reviews.interaction_models import ReviewInteraction

# إنشاء مستخدمين
try:
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='admin123',
        role='admin'
    )
    print("✅ تم إنشاء المستخدم Admin")
except Exception as e:
    print(f"❌ خطأ في إنشاء Admin: {e}")

try:
    user1 = User.objects.create_user(
        username='user1',
        email='user1@example.com',
        password='user123',
        role='user'
    )
    print("✅ تم إنشاء المستخدم User1")
except Exception as e:
    print(f"❌ خطأ في إنشاء User1: {e}")

try:
    user2 = User.objects.create_user(
        username='user2',
        email='user2@example.com',
        password='user123',
        role='user'
    )
    print("✅ تم إنشاء المستخدم User2")
except Exception as e:
    print(f"❌ خطأ في إنشاء User2: {e}")

# إنشاء منتجات
try:
    product1 = Product.objects.create(
        name='هاتف ذكي',
        description='هاتف ذكي حديث بمواصفات عالية',
        price=999.99,
        category='electronics',
        stock=50
    )
    print("✅ تم إنشاء المنتج الأول")
except Exception as e:
    print(f"❌ خطأ في إنشاء المنتج الأول: {e}")

try:
    product2 = Product.objects.create(
        name='لابتوب',
        description='لابتوب للألعاب والعمل',
        price=1999.99,
        category='electronics',
        stock=20
    )
    print("✅ تم إنشاء المنتج الثاني")
except Exception as e:
    print(f"❌ خطأ في إنشاء المنتج الثاني: {e}")

# إنشاء مراجعات
try:
    review1 = Review.objects.create(
        product=product1,
        user=user1,
        rating=5,
        text='منتج ممتاز جداً، أنصح به بشدة!',
        approval_status='approved'
    )
    print("✅ تم إنشاء المراجعة الأولى")
except Exception as e:
    print(f"❌ خطأ في إنشاء المراجعة الأولى: {e}")

try:
    review2 = Review.objects.create(
        product=product1,
        user=user2,
        rating=4,
        text='منتج جيد لكن يمكن تحسين البطارية',
        approval_status='approved'
    )
    print("✅ تم إنشاء المراجعة الثانية")
except Exception as e:
    print(f"❌ خطأ في إنشاء المراجعة الثانية: {e}")

try:
    review3 = Review.objects.create(
        product=product2,
        user=user1,
        rating=3,
        text='منتج عادي، لا بأس به',
        approval_status='pending'
    )
    print("✅ تم إنشاء المراجعة الثالثة")
except Exception as e:
    print(f"❌ خطأ في إنشاء المراجعة الثالثة: {e}")

# إنشاء تفاعلات
try:
    interaction1 = ReviewInteraction.objects.create(
        user=user2,
        review=review1,
        interaction_type='like'
    )
    print("✅ تم إنشاء التفاعل الأول")
except Exception as e:
    print(f"❌ خطأ في إنشاء التفاعل الأول: {e}")

try:
    interaction2 = ReviewInteraction.objects.create(
        user=user1,
        review=review2,
        interaction_type='like'
    )
    print("✅ تم إنشاء التفاعل الثاني")
except Exception as e:
    print(f"❌ خطأ في إنشاء التفاعل الثاني: {e}")

print("\n" + "="*50)
print("🎉 تم الانتهاء من إنشاء البيانات التجريبية!")
print("="*50)
print("📋 معلومات الدخول:")
print("- Admin: admin / admin123")
print("- User1: user1 / user123")
print("- User2: user2 / user123")
print("="*50)
print("🔗 الروابط للاختبار:")
print("- Django Admin: http://localhost:3000/admin/")
print("- Reviews API: http://localhost:3000/reviews/analytics/general/")
print("- Product Analytics: http://localhost:3000/products/1/analytics/")
print("="*50)

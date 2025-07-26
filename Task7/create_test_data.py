
import os
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_reviews.settings')
django.setup()

from accounts.models import User
from products.models import Product
from reviews.models import Review
from reviews.interactions_models import ReviewInteraction
from datetime import datetime, timedelta
import random

def create_test_data():
    """إنشاء بيانات تجريبية شاملة"""
    print("🔄 بدء إنشاء البيانات التجريبية...")
    
    # إنشاء مستخدمين
    print("👥 إنشاء مستخدمين...")
    users_data = [
        {"username": "user1", "email": "user1@example.com", "first_name": "أحمد", "last_name": "محمد"},
        {"username": "user2", "email": "user2@example.com", "first_name": "فاطمة", "last_name": "علي"},
        {"username": "user3", "email": "user3@example.com", "first_name": "محمد", "last_name": "حسن"},
        {"username": "admin", "email": "admin@example.com", "first_name": "مدير", "last_name": "النظام"},
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data["username"],
            defaults={
                "email": user_data["email"],
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "role": "admin" if user_data["username"] == "admin" else "customer"
            }
        )
        if created:
            user.set_password("testpass123")
            user.save()
        created_users.append(user)
        print(f"   ✅ {user.username}")
    
    # إنشاء منتجات
    print("\n📦 إنشاء منتجات...")
    products_data = [
        {"name": "iPhone 15 Pro", "description": "هاتف ذكي متطور", "price": 1200.00, "category": "إلكترونيات"},
        {"name": "Samsung Galaxy S24", "description": "هاتف أندرويد ممتاز", "price": 1000.00, "category": "إلكترونيات"},
        {"name": "MacBook Air M2", "description": "لابتوب للمحترفين", "price": 1500.00, "category": "حاسوب"},
        {"name": "AirPods Pro", "description": "سماعات لاسلكية", "price": 200.00, "category": "إكسسوارات"},
        {"name": "Apple Watch", "description": "ساعة ذكية", "price": 400.00, "category": "إكسسوارات"},
    ]
    
    created_products = []
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data["name"],
            defaults=product_data
        )
        created_products.append(product)
        print(f"   ✅ {product.name}")
    
    # إنشاء مراجعات متنوعة
    print("\n📝 إنشاء مراجعات...")
    reviews_data = [
        {"rating": 5, "text": "منتج ممتاز جداً! أنصح بشرائه بقوة", "approval_status": "approved"},
        {"rating": 4, "text": "جيد جداً، يستحق المال المدفوع", "approval_status": "approved"},
        {"rating": 5, "text": "رائع! فاق توقعاتي", "approval_status": "approved"},
        {"rating": 3, "text": "عادي، لا بأس به", "approval_status": "approved"},
        {"rating": 2, "text": "ليس كما توقعت، مخيب للآمال", "approval_status": "approved"},
        {"rating": 1, "text": "سيء جداً، لا أنصح به", "approval_status": "approved"},
        {"rating": 5, "text": "الأفضل في فئته!", "approval_status": "pending"},
        {"rating": 4, "text": "جودة ممتازة ولكن السعر مرتفع", "approval_status": "rejected"},
    ]
    
    created_reviews = []
    for i, review_data in enumerate(reviews_data):
        # توزيع المراجعات على المنتجات والمستخدمين
        product = created_products[i % len(created_products)]
        user = created_users[i % len(created_users)]
        
        # تجنب التكرار للمستخدم والمنتج نفسه
        existing = Review.objects.filter(product=product, user=user).first()
        if existing:
            continue
            
        review = Review.objects.create(
            product=product,
            user=user,
            rating=review_data["rating"],
            text=review_data["text"],
            approval_status=review_data["approval_status"],
            views=random.randint(0, 100),
            created_at=datetime.now() - timedelta(days=random.randint(0, 60))
        )
        created_reviews.append(review)
        print(f"   ✅ مراجعة {review.rating} نجوم للمنتج {product.name}")
    
    # إنشاء تفاعلات
    print("\n💬 إنشاء تفاعلات...")
    interaction_types = ["helpful", "not_helpful"]
    
    for review in created_reviews:
        # إنشاء تفاعلات عشوائية
        num_interactions = random.randint(0, 10)
        for _ in range(num_interactions):
            user = random.choice(created_users)
            interaction_type = random.choice(interaction_types)
            
            # تجنب التفاعل المكرر من نفس المستخدم
            existing = ReviewInteraction.objects.filter(
                review=review, 
                user=user
            ).first()
            if existing:
                continue
                
            ReviewInteraction.objects.create(
                review=review,
                user=user,
                interaction_type=interaction_type
            )
        
        interactions_count = review.interactions.count()
        if interactions_count > 0:
            print(f"   ✅ {interactions_count} تفاعل للمراجعة {review.id}")
    
    print("\n🎉 تم إنشاء البيانات التجريبية بنجاح!")
    print(f"📊 الإحصائيات:")
    print(f"   👥 المستخدمين: {User.objects.count()}")
    print(f"   📦 المنتجات: {Product.objects.count()}")
    print(f"   📝 المراجعات: {Review.objects.count()}")
    print(f"   💬 التفاعلات: {ReviewInteraction.objects.count()}")

if __name__ == "__main__":
    create_test_data()

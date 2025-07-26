
import requests
import json

# إعداد الخادم
BASE_URL = "http://127.0.0.1:8000/api"

def test_analytics_and_interactions():
    """
    اختبار شامل للتحليلات والتفاعل
    """
    print("🔍 بدء اختبار APIs التحليلات والتفاعل...")
    
    # 1. تسجيل دخول المستخدم للحصول على Token
    print("\n1️⃣ تسجيل دخول المستخدم...")
    login_data = {
        "email": "user@example.com",
        "password": "testpass123"
    }
    
    login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    if login_response.status_code == 200:
        token = login_response.json()['access']
        headers = {'Authorization': f'Bearer {token}'}
        print("✅ تم تسجيل الدخول بنجاح")
    else:
        print("❌ فشل في تسجيل الدخول")
        return
    
    # 2. اختبار التفاعل مع مراجعة
    print("\n2️⃣ اختبار التفاعل مع مراجعة...")
    review_id = 1  # تأكد من وجود مراجعة بهذا الرقم
    interaction_data = {
        "interaction_type": "helpful"
    }
    
    interaction_response = requests.post(
        f"{BASE_URL}/reviews/{review_id}/like/",
        json=interaction_data,
        headers=headers
    )
    
    if interaction_response.status_code in [200, 201]:
        print("✅ تم تسجيل التفاعل بنجاح")
        print(json.dumps(interaction_response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"❌ فشل في التفاعل: {interaction_response.status_code}")
        print(interaction_response.text)
    
    # 3. اختبار تحليلات المنتج
    print("\n3️⃣ اختبار تحليلات المنتج...")
    product_id = 1  # تأكد من وجود منتج بهذا الرقم
    
    analytics_response = requests.get(
        f"{BASE_URL}/reviews/analytics/products/{product_id}/?days=30"
    )
    
    if analytics_response.status_code == 200:
        print("✅ تم الحصول على تحليلات المنتج بنجاح")
        print(json.dumps(analytics_response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"❌ فشل في الحصول على التحليلات: {analytics_response.status_code}")
    
    # 4. اختبار البحث بالكلمات المفتاحية
    print("\n4️⃣ اختبار البحث بالكلمات المفتاحية...")
    
    search_response = requests.get(
        f"{BASE_URL}/reviews/analytics/search/?keyword=ممتاز"
    )
    
    if search_response.status_code == 200:
        print("✅ تم البحث بنجاح")
        print(json.dumps(search_response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"❌ فشل في البحث: {search_response.status_code}")
    
    # 5. اختبار أفضل المنتجات
    print("\n5️⃣ اختبار أفضل المنتجات...")
    
    top_products_response = requests.get(
        f"{BASE_URL}/reviews/analytics/top-products/?days=30"
    )
    
    if top_products_response.status_code == 200:
        print("✅ تم الحصول على أفضل المنتجات بنجاح")
        print(json.dumps(top_products_response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"❌ فشل في الحصول على أفضل المنتجات: {top_products_response.status_code}")
    
    # 6. اختبار الترتيب والتصفية
    print("\n6️⃣ اختبار الترتيب والتصفية...")
    
    # اختبار ترتيب المراجعات حسب الأعلى تقييم
    print("\n📋 اختبار ترتيب حسب الأعلى تقييم...")
    highest_rated_response = requests.get(
        f"{BASE_URL}/reviews/?ordering=highest_rated"
    )
    
    if highest_rated_response.status_code == 200:
        print("✅ تم الترتيب حسب الأعلى تقييم بنجاح")
        reviews = highest_rated_response.json().get('results', [])
        if reviews:
            print(f"أول مراجعة: {reviews[0].get('rating')} نجوم")
    
    # اختبار تصفية المراجعات 5 نجوم فقط
    print("\n⭐ اختبار تصفية مراجعات 5 نجوم...")
    five_star_response = requests.get(
        f"{BASE_URL}/reviews/?rating=5"
    )
    
    if five_star_response.status_code == 200:
        print("✅ تم تصفية مراجعات 5 نجوم بنجاح")
        reviews = five_star_response.json().get('results', [])
        print(f"عدد مراجعات 5 نجوم: {len(reviews)}")
    
    # اختبار ترتيب حسب الأكثر تفاعلاً
    print("\n🔥 اختبار ترتيب حسب الأكثر تفاعلاً...")
    most_interactive_response = requests.get(
        f"{BASE_URL}/reviews/?ordering=most_interactive"
    )
    
    if most_interactive_response.status_code == 200:
        print("✅ تم الترتيب حسب الأكثر تفاعلاً بنجاح")
    
    # اختبار تصفية المراجعات عالية التقييم (4-5 نجوم)
    print("\n🌟 اختبار تصفية المراجعات عالية التقييم...")
    high_rating_response = requests.get(
        f"{BASE_URL}/reviews/?high_rating_only=true"
    )
    
    if high_rating_response.status_code == 200:
        print("✅ تم تصفية المراجعات عالية التقييم بنجاح")
        reviews = high_rating_response.json().get('results', [])
        print(f"عدد المراجعات عالية التقييم: {len(reviews)}")
    
    # اختبار ترتيب حسب الأكثر مشاهدة
    print("\n👁️ اختبار ترتيب حسب الأكثر مشاهدة...")
    most_viewed_response = requests.get(
        f"{BASE_URL}/reviews/?ordering=most_viewed"
    )
    
    if most_viewed_response.status_code == 200:
        print("✅ تم الترتيب حسب الأكثر مشاهدة بنجاح")

if __name__ == "__main__":
    test_analytics_and_interactions()

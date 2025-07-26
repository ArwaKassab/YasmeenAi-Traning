
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

if __name__ == "__main__":
    test_analytics_and_interactions()

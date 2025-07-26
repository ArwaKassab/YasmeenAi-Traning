
import requests
import json
from datetime import datetime, timedelta

# إعداد الخادم
BASE_URL = "http://127.0.0.1:8000/api"

def get_auth_headers():
    """الحصول على headers التصريح"""
    print("🔐 تسجيل الدخول...")
    login_data = {
        "email": "user@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            token = response.json()['access']
            print("✅ تم تسجيل الدخول بنجاح")
            return {'Authorization': f'Bearer {token}'}
        else:
            print("❌ فشل في تسجيل الدخول")
            return {}
    except:
        print("⚠️ تخطي التصريح - سيتم استخدام الوصول العام فقط")
        return {}

def test_basic_listing():
    """اختبار عرض المراجعات الأساسي"""
    print("\n" + "="*50)
    print("📋 اختبار عرض المراجعات الأساسي")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/reviews/")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ إجمالي المراجعات: {len(data.get('results', []))}")
        if data.get('results'):
            review = data['results'][0]
            print(f"   📝 أول مراجعة: {review.get('rating', 'N/A')} نجوم")
            print(f"   👤 بواسطة: {review.get('user', {}).get('username', 'غير معروف')}")
    else:
        print(f"❌ فشل في الحصول على المراجعات: {response.status_code}")

def test_rating_filters():
    """اختبار تصفية حسب التقييم"""
    print("\n" + "="*50)
    print("⭐ اختبار تصفية حسب التقييم")
    print("="*50)
    
    # تصفية مراجعات 5 نجوم
    print("\n🌟 مراجعات 5 نجوم:")
    response = requests.get(f"{BASE_URL}/reviews/?rating=5")
    if response.status_code == 200:
        count = len(response.json().get('results', []))
        print(f"   عدد مراجعات 5 نجوم: {count}")
    
    # تصفية مراجعات عالية التقييم (4-5 نجوم)
    print("\n✨ مراجعات عالية التقييم (4-5 نجوم):")
    response = requests.get(f"{BASE_URL}/reviews/?high_rating_only=true")
    if response.status_code == 200:
        count = len(response.json().get('results', []))
        print(f"   عدد المراجعات عالية التقييم: {count}")
    
    # تصفية مراجعات منخفضة التقييم (1-2 نجمة)
    print("\n⭐ مراجعات منخفضة التقييم (1-2 نجمة):")
    response = requests.get(f"{BASE_URL}/reviews/?low_rating_only=true")
    if response.status_code == 200:
        count = len(response.json().get('results', []))
        print(f"   عدد المراجعات منخفضة التقييم: {count}")
    
    # تصفية حسب نطاق التقييم
    print("\n📊 مراجعات من 3 نجوم فأكثر:")
    response = requests.get(f"{BASE_URL}/reviews/?rating_min=3")
    if response.status_code == 200:
        count = len(response.json().get('results', []))
        print(f"   عدد المراجعات 3+ نجوم: {count}")

def test_ordering_options():
    """اختبار خيارات الترتيب"""
    print("\n" + "="*50)
    print("🔄 اختبار خيارات الترتيب")
    print("="*50)
    
    ordering_tests = [
        ("highest_rated", "الأعلى تقييماً"),
        ("most_interactive", "الأكثر تفاعلاً"),
        ("most_helpful", "الأكثر فائدة"),
        ("most_viewed", "الأكثر مشاهدة"),
        ("-created_at", "الأحدث أولاً"),
        ("created_at", "الأقدم أولاً")
    ]
    
    for ordering, description in ordering_tests:
        print(f"\n📈 {description}:")
        response = requests.get(f"{BASE_URL}/reviews/?ordering={ordering}")
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                review = results[0]
                print(f"   ✅ أول مراجعة: {review.get('rating', 'N/A')} نجوم")
                print(f"      مشاهدات: {review.get('views', 0)}")
                print(f"      تفاعلات: {review.get('total_interactions', 0)}")
            else:
                print("   📭 لا توجد نتائج")
        else:
            print(f"   ❌ فشل: {response.status_code}")

def test_product_filtering():
    """اختبار تصفية حسب المنتج"""
    print("\n" + "="*50)
    print("📦 اختبار تصفية حسب المنتج")
    print("="*50)
    
    # تصفية مراجعات منتج معين
    print("\n🎯 مراجعات المنتج رقم 1:")
    response = requests.get(f"{BASE_URL}/reviews/?product=1")
    if response.status_code == 200:
        count = len(response.json().get('results', []))
        print(f"   عدد مراجعات المنتج 1: {count}")
    
    # البحث في أسماء المنتجات
    print("\n🔍 البحث في أسماء المنتجات (iPhone):")
    response = requests.get(f"{BASE_URL}/reviews/?product_name=iPhone")
    if response.status_code == 200:
        count = len(response.json().get('results', []))
        print(f"   عدد المراجعات لمنتجات iPhone: {count}")

def test_date_filtering():
    """اختبار تصفية حسب التاريخ"""
    print("\n" + "="*50)
    print("📅 اختبار تصفية حسب التاريخ")
    print("="*50)
    
    # آخر 7 أيام
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    print(f"\n📆 مراجعات آخر 7 أيام (من {week_ago}):")
    response = requests.get(f"{BASE_URL}/reviews/?date_from={week_ago}")
    if response.status_code == 200:
        count = len(response.json().get('results', []))
        print(f"   عدد المراجعات في آخر 7 أيام: {count}")
    
    # آخر 30 يوم
    month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    print(f"\n📅 مراجعات آخر 30 يوم (من {month_ago}):")
    response = requests.get(f"{BASE_URL}/reviews/?date_from={month_ago}")
    if response.status_code == 200:
        count = len(response.json().get('results', []))
        print(f"   عدد المراجعات في آخر 30 يوم: {count}")

def test_views_filtering():
    """اختبار تصفية حسب المشاهدات"""
    print("\n" + "="*50)
    print("👁️ اختبار تصفية حسب المشاهدات")
    print("="*50)
    
    # مراجعات بمشاهدات عالية
    print("\n🔥 مراجعات بـ 10 مشاهدات فأكثر:")
    response = requests.get(f"{BASE_URL}/reviews/?min_views=10")
    if response.status_code == 200:
        count = len(response.json().get('results', []))
        print(f"   عدد المراجعات عالية المشاهدات: {count}")
    
    # مراجعات بمشاهدات قليلة
    print("\n👀 مراجعات بـ 5 مشاهدات فأقل:")
    response = requests.get(f"{BASE_URL}/reviews/?max_views=5")
    if response.status_code == 200:
        count = len(response.json().get('results', []))
        print(f"   عدد المراجعات قليلة المشاهدات: {count}")

def test_interaction_filtering():
    """اختبار تصفية حسب التفاعلات"""
    print("\n" + "="*50)
    print("💬 اختبار تصفية حسب التفاعلات")
    print("="*50)
    
    headers = get_auth_headers()
    
    # مراجعات لديها تفاعلات
    print("\n🔄 مراجعات لديها تفاعلات:")
    response = requests.get(f"{BASE_URL}/reviews/?has_interactions=true", headers=headers)
    if response.status_code == 200:
        count = len(response.json().get('results', []))
        print(f"   عدد المراجعات التي لديها تفاعلات: {count}")
    else:
        print(f"   ⚠️ الحالة: {response.status_code}")

def test_search_functionality():
    """اختبار وظيفة البحث"""
    print("\n" + "="*50)
    print("🔍 اختبار وظيفة البحث")
    print("="*50)
    
    search_terms = ["ممتاز", "جيد", "سيء", "رائع"]
    
    for term in search_terms:
        print(f"\n🔎 البحث عن '{term}':")
        response = requests.get(f"{BASE_URL}/reviews/?search={term}")
        if response.status_code == 200:
            count = len(response.json().get('results', []))
            print(f"   عدد النتائج: {count}")
        else:
            print(f"   ❌ فشل: {response.status_code}")

def test_combined_filters():
    """اختبار دمج عدة فلاتر"""
    print("\n" + "="*50)
    print("🎯 اختبار دمج عدة فلاتر")
    print("="*50)
    
    combinations = [
        ("rating=5&ordering=most_interactive", "مراجعات 5 نجوم مرتبة حسب الأكثر تفاعلاً"),
        ("high_rating_only=true&ordering=-created_at", "مراجعات عالية مرتبة حسب الأحدث"),
        ("rating_min=4&min_views=5", "مراجعات 4+ نجوم بـ5+ مشاهدات"),
        ("low_rating_only=true&ordering=most_viewed", "مراجعات منخفضة مرتبة حسب الأكثر مشاهدة")
    ]
    
    for params, description in combinations:
        print(f"\n🎪 {description}:")
        response = requests.get(f"{BASE_URL}/reviews/?{params}")
        if response.status_code == 200:
            count = len(response.json().get('results', []))
            print(f"   عدد النتائج: {count}")
            if count > 0:
                review = response.json()['results'][0]
                print(f"   أول نتيجة: {review.get('rating')} نجوم, {review.get('views', 0)} مشاهدة")
        else:
            print(f"   ❌ فشل: {response.status_code}")

def test_approval_status_filtering():
    """اختبار تصفية حسب حالة الموافقة"""
    print("\n" + "="*50)
    print("✅ اختبار تصفية حسب حالة الموافقة")
    print("="*50)
    
    headers = get_auth_headers()
    
    statuses = [
        ("pending", "معلقة"),
        ("approved", "معتمدة"),
        ("rejected", "مرفوضة")
    ]
    
    for status_val, description in statuses:
        print(f"\n📋 مراجعات {description}:")
        response = requests.get(f"{BASE_URL}/reviews/?approval_status={status_val}", headers=headers)
        if response.status_code == 200:
            count = len(response.json().get('results', []))
            print(f"   عدد المراجعات {description}: {count}")
        else:
            print(f"   ⚠️ الحالة: {response.status_code}")

def run_comprehensive_test():
    """تشغيل اختبار شامل لجميع الميزات"""
    print("🚀 بدء الاختبار الشامل لميزات الترتيب والتصفية")
    print("="*60)
    
    try:
        test_basic_listing()
        test_rating_filters()
        test_ordering_options()
        test_product_filtering()
        test_date_filtering()
        test_views_filtering()
        test_interaction_filtering()
        test_search_functionality()
        test_combined_filters()
        test_approval_status_filtering()
        
        print("\n" + "="*60)
        print("✅ تم الانتهاء من جميع الاختبارات!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ حدث خطأ أثناء الاختبار: {e}")

if __name__ == "__main__":
    run_comprehensive_test()

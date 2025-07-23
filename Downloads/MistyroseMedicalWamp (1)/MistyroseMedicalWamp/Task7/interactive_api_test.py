
#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:3000"

def get_auth_token():
    """الحصول على توكن المصادقة"""
    try:
        response = requests.post(f'{BASE_URL}/api/auth/login/', {
            'email': 'admin@example.com',
            'password': 'admin123'
        })
        if response.status_code == 200:
            return response.json().get('access')
        return None
    except:
        return None

def test_api_endpoint(url, method='GET', auth_required=False, body=None):
    """اختبار نقطة API واحدة"""
    headers = {'Content-Type': 'application/json'}
    
    if auth_required:
        token = get_auth_token()
        if token:
            headers['Authorization'] = f'Bearer {token}'
        else:
            print("❌ فشل في الحصول على توكن المصادقة")
            return
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=body, headers=headers)
        
        print(f"📊 حالة الاستجابة: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"📈 عدد النتائج: {len(data)}")
                if data:
                    print("🔍 أول 3 نتائج:")
                    for i, item in enumerate(data[:3]):
                        rating = item.get('rating', 'N/A')
                        text = item.get('text', '')[:50] + '...' if len(item.get('text', '')) > 50 else item.get('text', '')
                        created = item.get('created_at', '')[:10] if item.get('created_at') else 'N/A'
                        print(f"      {i+1}. تقييم: {rating}⭐ - {text} ({created})")
            else:
                print(f"📋 البيانات: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ خطأ: {response.text}")
            
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")

def main():
    """القائمة التفاعلية"""
    print("🎯 اختبار تفاعلي لـ API الترتيب والتصفية")
    print("=" * 50)
    
    while True:
        print("\n📋 اختر الاختبار:")
        print("1. الترتيب حسب الأحدث (افتراضي)")
        print("2. الترتيب حسب أعلى تقييم")
        print("3. الترتيب حسب الأكثر تفاعلاً")
        print("4. تصفية مراجعات 5 نجوم")
        print("5. تصفية مراجعات 4 نجوم")
        print("6. دمج: 5 نجوم + الأكثر تفاعلاً")
        print("7. دمج: 4 نجوم + الأحدث")
        print("8. جميع المراجعات (يتطلب مصادقة)")
        print("9. اختبار مخصص")
        print("0. خروج")
        
        choice = input("\n🔤 اختر رقم الاختبار: ")
        
        if choice == '0':
            print("👋 وداعاً!")
            break
        elif choice == '1':
            print("\n🕐 اختبار الترتيب حسب الأحدث...")
            test_api_endpoint(f"{BASE_URL}/api/reviews/product/1/")
        elif choice == '2':
            print("\n⭐ اختبار الترتيب حسب أعلى تقييم...")
            test_api_endpoint(f"{BASE_URL}/api/reviews/product/1/?ordering=-rating")
        elif choice == '3':
            print("\n🔥 اختبار الترتيب حسب الأكثر تفاعلاً...")
            test_api_endpoint(f"{BASE_URL}/api/reviews/product/1/?ordering=-interaction_score")
        elif choice == '4':
            print("\n🌟 اختبار تصفية مراجعات 5 نجوم...")
            test_api_endpoint(f"{BASE_URL}/api/reviews/product/1/?stars=5")
        elif choice == '5':
            print("\n⭐ اختبار تصفية مراجعات 4 نجوم...")
            test_api_endpoint(f"{BASE_URL}/api/reviews/product/1/?stars=4")
        elif choice == '6':
            print("\n🔥🌟 اختبار دمج: 5 نجوم + الأكثر تفاعلاً...")
            test_api_endpoint(f"{BASE_URL}/api/reviews/product/1/?stars=5&ordering=-interaction_score")
        elif choice == '7':
            print("\n🕐⭐ اختبار دمج: 4 نجوم + الأحدث...")
            test_api_endpoint(f"{BASE_URL}/api/reviews/product/1/?stars=4&ordering=-created_at")
        elif choice == '8':
            print("\n📊 اختبار جميع المراجعات...")
            test_api_endpoint(f"{BASE_URL}/api/reviews/?ordering=-created_at", auth_required=True)
        elif choice == '9':
            print("\n🔧 اختبار مخصص")
            endpoint = input("🔗 أدخل endpoint (مثل: /api/reviews/product/1/?stars=3): ")
            test_api_endpoint(f"{BASE_URL}{endpoint}")
        else:
            print("❌ اختيار غير صحيح")

if __name__ == '__main__':
    main()

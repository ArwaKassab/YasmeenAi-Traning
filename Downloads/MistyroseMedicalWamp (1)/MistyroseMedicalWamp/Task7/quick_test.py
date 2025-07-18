
#!/usr/bin/env python3
import requests

BASE_URL = "http://localhost:3000"

def quick_test():
    print("🚀 اختبار سريع للترتيب والتصفية")
    print("="*50)
    
    # اختبار بدون مصادقة (مراجعات المنتج)
    tests = [
        ("الأحدث أولاً", "/api/reviews/product/1/"),
        ("أعلى تقييم", "/api/reviews/product/1/?ordering=-rating"),
        ("الأكثر تفاعلاً", "/api/reviews/product/1/?ordering=-interaction_score"),
        ("5 نجوم فقط", "/api/reviews/product/1/?stars=5"),
        ("4 نجوم + أعلى تقييم", "/api/reviews/product/1/?stars=4&ordering=-rating")
    ]
    
    for name, endpoint in tests:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else len(data.get('results', []))
                print(f"✅ {name}: {count} نتيجة")
            else:
                print(f"❌ {name}: خطأ {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: خطأ اتصال")

if __name__ == "__main__":
    quick_test()

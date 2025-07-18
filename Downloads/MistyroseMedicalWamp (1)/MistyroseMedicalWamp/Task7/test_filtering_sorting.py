
#!/usr/bin/env python3
"""
ملف اختبار خيارات الترتيب والتصفية للمراجعات
"""

import requests
import json
import sys

BASE_URL = "http://localhost:3000"

def get_auth_token():
    """الحصول على توكن المصادقة"""
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
    if response.status_code == 200:
        return response.json()["tokens"]["access"]
    else:
        print("فشل في تسجيل الدخول:", response.text)
        return None

def test_sorting_and_filtering():
    """اختبار خيارات الترتيب والتصفية"""
    
    print("🔄 جاري الحصول على توكن المصادقة...")
    token = get_auth_token()
    if not token:
        print("❌ فشل في الحصول على التوكن")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n" + "="*60)
    print("📊 اختبار خيارات الترتيب والتصفية للمراجعات")
    print("="*60)
    
    # اختبارات الترتيب
    sorting_tests = [
        {
            "name": "الترتيب حسب الأحدث (افتراضي)",
            "url": f"{BASE_URL}/api/reviews/",
            "description": "عرض المراجعات مرتبة حسب تاريخ الإنشاء (الأحدث أولاً)"
        },
        {
            "name": "الترتيب حسب الأقدم",
            "url": f"{BASE_URL}/api/reviews/?ordering=created_at",
            "description": "عرض المراجعات مرتبة حسب تاريخ الإنشاء (الأقدم أولاً)"
        },
        {
            "name": "الترتيب حسب أعلى تقييم",
            "url": f"{BASE_URL}/api/reviews/?ordering=-rating",
            "description": "عرض المراجعات مرتبة حسب التقييم (الأعلى أولاً)"
        },
        {
            "name": "الترتيب حسب أقل تقييم",
            "url": f"{BASE_URL}/api/reviews/?ordering=rating",
            "description": "عرض المراجعات مرتبة حسب التقييم (الأقل أولاً)"
        },
        {
            "name": "الترتيب حسب الأكثر إعجاباً",
            "url": f"{BASE_URL}/api/reviews/?ordering=-likes_count",
            "description": "عرض المراجعات مرتبة حسب عدد الإعجابات (الأكثر أولاً)"
        },
        {
            "name": "الترتيب حسب الأكثر تفاعلاً",
            "url": f"{BASE_URL}/api/reviews/?ordering=-interaction_score",
            "description": "عرض المراجعات مرتبة حسب نقاط التفاعل (الإعجابات - عدم الإعجاب)"
        }
    ]
    
    # اختبارات التصفية
    filtering_tests = [
        {
            "name": "تصفية مراجعات 5 نجوم فقط",
            "url": f"{BASE_URL}/api/reviews/?stars=5",
            "description": "عرض المراجعات ذات 5 نجوم فقط"
        },
        {
            "name": "تصفية مراجعات 4 نجوم فقط",
            "url": f"{BASE_URL}/api/reviews/?stars=4",
            "description": "عرض المراجعات ذات 4 نجوم فقط"
        },
        {
            "name": "تصفية مراجعات منتج محدد",
            "url": f"{BASE_URL}/api/reviews/?product_id=1",
            "description": "عرض مراجعات المنتج رقم 1 فقط"
        },
        {
            "name": "تصفية وترتيب معاً (5 نجوم + الأكثر تفاعلاً)",
            "url": f"{BASE_URL}/api/reviews/?stars=5&ordering=-interaction_score",
            "description": "مراجعات 5 نجوم مرتبة حسب التفاعل"
        }
    ]
    
    # اختبارات مراجعات منتج محدد
    product_tests = [
        {
            "name": "مراجعات المنتج 1 - الأحدث",
            "url": f"{BASE_URL}/api/reviews/product/1/?ordering=-created_at",
            "description": "مراجعات المنتج 1 مرتبة حسب الأحدث"
        },
        {
            "name": "مراجعات المنتج 1 - أعلى تقييم",
            "url": f"{BASE_URL}/api/reviews/product/1/?ordering=-rating",
            "description": "مراجعات المنتج 1 مرتبة حسب أعلى تقييم"
        },
        {
            "name": "مراجعات المنتج 1 - الأكثر تفاعلاً",
            "url": f"{BASE_URL}/api/reviews/product/1/?ordering=-interaction_score",
            "description": "مراجعات المنتج 1 مرتبة حسب التفاعل"
        },
        {
            "name": "مراجعات المنتج 1 - 5 نجوم فقط",
            "url": f"{BASE_URL}/api/reviews/product/1/?stars=5",
            "description": "مراجعات 5 نجوم للمنتج 1 فقط"
        }
    ]
    
    all_tests = [
        ("🔄 اختبارات الترتيب", sorting_tests, headers),
        ("🔍 اختبارات التصفية", filtering_tests, headers),
        ("📦 اختبارات مراجعات المنتج (بدون مصادقة)", product_tests, {})
    ]
    
    for section_name, tests, test_headers in all_tests:
        print(f"\n{section_name}")
        print("-" * 50)
        
        for test in tests:
            print(f"\n📝 {test['name']}")
            print(f"   📄 {test['description']}")
            print(f"   🔗 {test['url']}")
            
            try:
                response = requests.get(test['url'], headers=test_headers)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'results' in data:
                        results = data['results']
                    else:
                        results = data
                    
                    print(f"   ✅ نجح الاختبار - عدد النتائج: {len(results)}")
                    
                    # عرض أول 3 نتائج كعينة
                    if results:
                        print("   📊 عينة من النتائج:")
                        for i, result in enumerate(results[:3]):
                            rating = result.get('rating', 'غير متوفر')
                            likes = result.get('likes_count', 0)
                            score = result.get('interaction_score', 0)
                            created = result.get('created_at', 'غير متوفر')[:10] if result.get('created_at') else 'غير متوفر'
                            
                            print(f"      {i+1}. تقييم: {rating}⭐ | إعجابات: {likes} | نقاط التفاعل: {score} | تاريخ: {created}")
                    else:
                        print("   📝 لا توجد نتائج")
                        
                else:
                    print(f"   ❌ فشل الاختبار - كود الخطأ: {response.status_code}")
                    print(f"   📄 رسالة الخطأ: {response.text[:200]}")
                    
            except Exception as e:
                print(f"   ❌ خطأ في الاتصال: {str(e)}")
    
    print("\n" + "="*60)
    print("📋 ملخص خيارات الترتيب والتصفية المتاحة:")
    print("="*60)
    print("🔄 خيارات الترتيب (ordering):")
    print("   • -created_at : الأحدث أولاً (افتراضي)")
    print("   • created_at  : الأقدم أولاً")
    print("   • -rating     : أعلى تقييم أولاً")
    print("   • rating      : أقل تقييم أولاً")
    print("   • -likes_count: الأكثر إعجاباً أولاً")
    print("   • -interaction_score: الأكثر تفاعلاً أولاً")
    
    print("\n🔍 خيارات التصفية:")
    print("   • stars=5     : مراجعات 5 نجوم فقط")
    print("   • stars=4     : مراجعات 4 نجوم فقط")
    print("   • stars=3     : مراجعات 3 نجوم فقط")
    print("   • stars=2     : مراجعات 2 نجوم فقط")
    print("   • stars=1     : مراجعات 1 نجمة فقط")
    print("   • product_id=X: مراجعات منتج محدد")
    print("   • rating=X    : تصفية حسب التقييم (الطريقة القديمة)")
    
    print("\n💡 أمثلة على الاستخدام:")
    print("   • /api/reviews/?stars=5&ordering=-interaction_score")
    print("   • /api/reviews/product/1/?stars=4&ordering=-likes_count")
    print("   • /api/reviews/?product_id=2&ordering=-rating")

if __name__ == "__main__":
    test_sorting_and_filtering()

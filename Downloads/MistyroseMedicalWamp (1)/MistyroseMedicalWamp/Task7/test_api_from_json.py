
#!/usr/bin/env python3
import json
import requests
import sys
import os

def load_test_config():
    """تحميل إعدادات الاختبار من ملف JSON"""
    try:
        with open('api_tests.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ ملف api_tests.json غير موجود")
        return None
    except json.JSONDecodeError:
        print("❌ خطأ في تحليل ملف JSON")
        return None

def get_auth_token():
    """الحصول على توكن المصادقة"""
    try:
        response = requests.post('http://localhost:3000/api/auth/login/', {
            'email': 'admin@example.com',
            'password': 'admin123'
        })
        if response.status_code == 200:
            return response.json().get('access')
        else:
            print("❌ فشل في تسجيل الدخول")
            return None
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return None

def run_test(test_config, auth_token=None):
    """تشغيل اختبار واحد"""
    url = test_config.get('url', '')
    method = test_config.get('method', 'GET').upper()
    requires_auth = test_config.get('requires_auth', False)
    body = test_config.get('body', {})
    
    # إعداد الرؤوس
    headers = {'Content-Type': 'application/json'}
    if requires_auth and auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=body, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=body, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            print(f"❌ طريقة HTTP غير مدعومة: {method}")
            return False
        
        # عرض النتائج
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                count = len(data)
                print(f"✅ {test_config.get('name', 'اختبار')}: {count} نتيجة")
                if count > 0:
                    # عرض أول 3 نتائج
                    for i, item in enumerate(data[:3]):
                        rating = item.get('rating', 'N/A')
                        text = item.get('text', '')[:50] + '...' if len(item.get('text', '')) > 50 else item.get('text', '')
                        print(f"      {i+1}. تقييم: {rating}⭐ - {text}")
            elif isinstance(data, dict):
                results = data.get('results', [])
                count = len(results)
                print(f"✅ {test_config.get('name', 'اختبار')}: {count} نتيجة")
                if count > 0:
                    for i, item in enumerate(results[:3]):
                        rating = item.get('rating', 'N/A')
                        text = item.get('text', '')[:50] + '...' if len(item.get('text', '')) > 50 else item.get('text', '')
                        print(f"      {i+1}. تقييم: {rating}⭐ - {text}")
            else:
                print(f"✅ {test_config.get('name', 'اختبار')}: نجح")
        else:
            print(f"❌ {test_config.get('name', 'اختبار')}: خطأ {response.status_code}")
            if response.status_code == 401:
                print("   🔒 مطلوب مصادقة")
            elif response.status_code == 404:
                print("   🔍 الرابط غير موجود")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ {test_config.get('name', 'اختبار')}: خطأ في الاتصال - {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 تشغيل اختبارات API من ملف JSON")
    print("=" * 60)
    
    # تحميل إعدادات الاختبار
    config = load_test_config()
    if not config:
        return
    
    # الحصول على توكن المصادقة
    auth_token = get_auth_token()
    if not auth_token:
        print("⚠️ سيتم تشغيل الاختبارات بدون مصادقة")
    
    # اختبار المراجعات الأساسية
    print("\n📊 اختبار المراجعات الأساسية")
    print("-" * 40)
    basic_tests = config.get('reviews_api_tests', {}).get('endpoints', [])
    for test in basic_tests:
        full_url = f"http://localhost:3000{test['url']}"
        test_config = {**test, 'url': full_url}
        run_test(test_config, auth_token)
    
    # اختبار الترتيب والتصفية
    sorting_filtering = config.get('sorting_filtering_tests', {})
    
    if sorting_filtering:
        print("\n🔄 اختبار الترتيب")
        print("-" * 40)
        sorting_tests = sorting_filtering.get('sorting_tests', [])
        for test in sorting_tests:
            full_url = f"http://localhost:3000{test['url']}"
            test_config = {**test, 'url': full_url}
            run_test(test_config, auth_token)
        
        print("\n🎯 اختبار التصفية")
        print("-" * 40)
        filtering_tests = sorting_filtering.get('filtering_tests', [])
        for test in filtering_tests:
            full_url = f"http://localhost:3000{test['url']}"
            test_config = {**test, 'url': full_url}
            run_test(test_config, auth_token)
        
        print("\n🔀 اختبار الدمج (التصفية + الترتيب)")
        print("-" * 40)
        combined_tests = sorting_filtering.get('combined_tests', [])
        for test in combined_tests:
            full_url = f"http://localhost:3000{test['url']}"
            test_config = {**test, 'url': full_url}
            run_test(test_config, auth_token)
    
    print("\n✅ انتهت جميع الاختبارات")

if __name__ == '__main__':
    main()

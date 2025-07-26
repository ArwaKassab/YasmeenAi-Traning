
# دليل استخدام الترتيب والتصفية للمراجعات

## خيارات الترتيب المتاحة

### الترتيب القياسي
```
GET /api/reviews/?ordering=created_at        # الأحدث أولاً
GET /api/reviews/?ordering=-created_at       # الأقدم أولاً
GET /api/reviews/?ordering=rating           # الأقل تقييماً أولاً
GET /api/reviews/?ordering=-rating          # الأعلى تقييماً أولاً
```

### الترتيب المخصص
```
GET /api/reviews/?ordering=highest_rated     # الأعلى تقييماً
GET /api/reviews/?ordering=most_interactive  # الأكثر تفاعلاً
GET /api/reviews/?ordering=most_helpful      # الأكثر فائدة
GET /api/reviews/?ordering=most_viewed       # الأكثر مشاهدة
```

## خيارات التصفية المتاحة

### تصفية حسب التقييم
```
GET /api/reviews/?rating=5                   # مراجعات 5 نجوم فقط
GET /api/reviews/?rating_min=4               # مراجعات 4 نجوم فأكثر
GET /api/reviews/?rating_max=2               # مراجعات نجمتين فأقل
GET /api/reviews/?high_rating_only=true      # مراجعات عالية (4-5 نجوم)
GET /api/reviews/?low_rating_only=true       # مراجعات منخفضة (1-2 نجمة)
```

### تصفية حسب المنتج
```
GET /api/reviews/?product=1                  # مراجعات منتج معين
GET /api/reviews/?product_name=iPhone        # مراجعات منتجات تحتوي على "iPhone"
```

### تصفية حسب التاريخ
```
GET /api/reviews/?date_from=2024-01-01       # مراجعات من تاريخ معين
GET /api/reviews/?date_to=2024-12-31         # مراجعات حتى تاريخ معين
```

### تصفية حسب المشاهدات
```
GET /api/reviews/?min_views=100              # مراجعات بـ 100 مشاهدة فأكثر
GET /api/reviews/?max_views=50               # مراجعات بـ 50 مشاهدة فأقل
```

### تصفية حسب التفاعل
```
GET /api/reviews/?has_interactions=true      # مراجعات لديها تفاعلات
```

### تصفية حسب المستخدم
```
GET /api/reviews/?user=1                     # مراجعات مستخدم معين
GET /api/reviews/?user_name=ahmed            # مراجعات مستخدمين أسماؤهم تحتوي على "ahmed"
```

### تصفية حسب حالة الموافقة (للمدراء)
```
GET /api/reviews/?approval_status=pending    # مراجعات معلقة
GET /api/reviews/?approval_status=approved   # مراجعات معتمدة
GET /api/reviews/?approval_status=rejected   # مراجعات مرفوضة
```

## دمج الخيارات

يمكن دمج عدة خيارات معاً:

```
# مراجعات 5 نجوم مرتبة حسب الأكثر تفاعلاً
GET /api/reviews/?rating=5&ordering=most_interactive

# مراجعات عالية التقييم من آخر 30 يوم مرتبة حسب الأحدث
GET /api/reviews/?high_rating_only=true&date_from=2024-01-01&ordering=-created_at

# مراجعات منتج معين مرتبة حسب الأكثر فائدة
GET /api/reviews/products/1/?ordering=most_helpful
```

## البحث النصي

```
GET /api/reviews/?search=ممتاز               # البحث في نص المراجعات
GET /api/reviews/?search=iPhone              # البحث في اسم المنتج ونص المراجعة
```

## أمثلة عملية

### الحصول على أفضل مراجعات لمنتج معين
```
GET /api/reviews/products/1/?rating_min=4&ordering=most_helpful
```

### الحصول على أحدث مراجعات سلبية
```
GET /api/reviews/?low_rating_only=true&ordering=-created_at
```

### الحصول على المراجعات الأكثر تفاعلاً من آخر أسبوع
```
GET /api/reviews/?has_interactions=true&date_from=2024-01-15&ordering=most_interactive
```

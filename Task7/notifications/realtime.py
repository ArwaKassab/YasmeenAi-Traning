# notifications/realtime.py

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_user(review):
    """
    إرسال إشعار لحظي للمستخدم عند الموافقة على مراجعته.
    """
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{review.user.id}",  # اسم الجروب الخاص بالمستخدم
        {
            "type": "send_notification",  # اسم الدالة داخل الـ Consumer
            "message": f"✅ تمت الموافقة على مراجعتك للمنتج: {review.product.name}"
        }
    )

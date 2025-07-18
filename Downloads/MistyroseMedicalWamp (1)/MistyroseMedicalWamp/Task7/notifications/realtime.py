# notifications/realtime.py

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_user(review):
    """
    إرسال إشعار لحظي للمستخدم عند الموافقة على مراجعته.
    """
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{review.user.id}",  
        {
            "type": "send_notification",  
            "message": f"✅ تمت الموافقة على مراجعتك للمنتج: {review.product.name}"
        }
    )

def notify_review_reply(comment):
    """
    إرسال إشعار لحظي لصاحب المراجعة عند تلقي رد.
    """
    channel_layer = get_channel_layer()

    review = comment.review
    review_owner = review.user
    commenter = comment.user

    if review_owner != commenter:  
        async_to_sync(channel_layer.group_send)(
            f"user_{review_owner.id}", 
            {
                "type": "send_notification",
                "message": f"💬 {commenter.username} قام بالرد على مراجعتك: {comment.text}"
            }
        )

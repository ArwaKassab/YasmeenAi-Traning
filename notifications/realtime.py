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
            "message": f"✅تمت الموافقة على مراجعتك للمنتج: {review.product.name}",
            "review_id": review.id,
            "review_text": review.text  # تأكدي من اسم الحقل الصحيح في موديل Review
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
                "message": f"💬 {commenter.username} قام بالرد على مراجعتك: {comment.text}",
                "review_id": review.id,
                "review_text": review.text
            }
        )

def notify_user_deletion(data):
    """
    إشعار لحظي للمستخدم عند حذف مراجعته بسبب بلاغ.
    يستقبل البيانات بدلاً من كائن Review لأنه تم حذفه.
    """
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{data['user_id']}",
        {
            "type": "send_notification",
            "message": f"🚫 تم حذف مراجعتك عن المنتج: {data['product_name']} بعد بلاغ من أحد المستخدمين.",
            "review_text": data.get("review_text", "")
        }
    )

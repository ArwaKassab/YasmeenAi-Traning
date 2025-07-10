# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from product_reviews.middleware import JWTAuthMiddleware
import notifications.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_reviews.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(  # middleware الجديدة
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    ),
})

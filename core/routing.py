from django.urls import re_path
from core.consumers import ChatConsumer, WatchPartyConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>[\w-]+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/watchparty/(?P<room_name>[\w-]+)/$", WatchPartyConsumer.as_asgi()),
]

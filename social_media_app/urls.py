from __future__ import annotations

from django.urls import include
from django.urls import path

urlpatterns = [
    path('', include('user_auth.urls')),
    path('<str:user_id>/search_user/', include('search_user.urls')),
    path('<str:user_id>/friend/', include('friend_logic.urls')),
]

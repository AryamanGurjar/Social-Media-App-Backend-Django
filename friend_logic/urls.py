from __future__ import annotations

from django.urls import path

from .views import *

urlpatterns = [
    path('send_friend_request/', FriendRequestView.as_view(), name='send-request'),
    path(
        'request_action/', FriendRequestActionView.as_view(),
        name='action-on-request',
    ),
    path(
        'user_accepted_friends/', FriendsListView.as_view(),
        name='accept-request-list',
    ),
    path(
        'user_pending_friends/', PendingFriendRequestsView.as_view(),
        name='pending-request-list',
    ),
]

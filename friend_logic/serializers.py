from __future__ import annotations

from rest_framework import serializers

from friend_logic.models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'timestamp', 'status']

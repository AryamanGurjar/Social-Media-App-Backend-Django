from __future__ import annotations

from rest_framework import serializers

from user_auth.models import User


class UserSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields_param = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)
        # allow only some specific field to serialize.
        if fields_param is not None:
            allowed_fields = set(fields_param)
            existing_fields = set(self.fields.keys())

            for field_name in existing_fields - allowed_fields:
                self.fields.pop(field_name)

    class Meta:
        model = User
        fields = ['name', 'email']  # No default fields

from rest_framework import serializers
from user_auth.models import User

from social_media_app.utils import encode_text, decode_text

from user_auth.constants import EMPTY_PASSWORD, USER_ALREADY_EXIST

from social_media_app.custom_exception import InvalidValue

from search_user.constants import EMAIL_IDENTIFIER

from user_auth.constants import NO_PROPER_VALUE, INVALID_PASSWORD, INVALID_EMAIL, ENCRYPTED_PASSWORD




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        password = validated_data.pop('password')
        encrypted_password = encode_text(password)
        validated_data['password'] = encrypted_password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            encrypted_password = encode_text(password)
            validated_data['password'] = encrypted_password
        return super().update(instance, validated_data)

    def validate(self, data):
        """
        Checks no same email comes again. Also validate password.
        """
        email = data.get('email')
        if EMAIL_IDENTIFIER not in email:
            raise InvalidValue(message=INVALID_EMAIL)
        if User.objects.filter(email=email):
            raise serializers.ValidationError(USER_ALREADY_EXIST)
        if 'password' in data:
            password = data['password']
            if not password:
                raise serializers.ValidationError(EMPTY_PASSWORD)
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(instance.id)
        representation['password'] = ENCRYPTED_PASSWORD
        return representation




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validates user password and email id is correct or not.
        """
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = User.objects.filter(email=email)

            if not user:
                raise serializers.ValidationError(INVALID_EMAIL)
            user = user.first()
            user_password = self.decode_password(user)

            if user_password != password:
                raise serializers.ValidationError(INVALID_PASSWORD)

        else:
            raise InvalidValue(message= NO_PROPER_VALUE)

        data['user'] = user
        return data

    def decode_password(self, instance):
        encrypted_password = instance.password
        decrypted_password = decode_text(encrypted_password)
        return decrypted_password
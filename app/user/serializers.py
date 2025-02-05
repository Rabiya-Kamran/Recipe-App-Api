"""
Serializers for the user API View.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
    )
from django.utils.translation import gettext as _

from rest_framework import serializers


# ModelSerializer is a baseclass,
# which automatically maps the model fields to API fields
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
# we defne model and fields in META
# and any additional arguments to define in serializer
    class Meta:
        model = get_user_model()
        # Defines which fields to include in the API request/response
        fields = ['email', 'password', 'name']
        # extra_kwargs set extra validation rules
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

# validated_data contains the cleaned user data.
# validated_data comes from serializer only after validation
# called only when data is validated
    def create(self, validated_data):
        """Create and return a user with encrypted pwd"""
        return get_user_model().objects.create_user(**validated_data)

# instance being updated
# validated by serializers
    def update(self, instance, validated_data):
        """Update and return user. """
# remove password from validated_data
        password = validated_data.pop('password', None)
# Calls the parent class’s update method to
# update all other user details
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')
        # authenticate function is built in
        print(f"Authenticating user: {email}")
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to aunthenticate wth provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

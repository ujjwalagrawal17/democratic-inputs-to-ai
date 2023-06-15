from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import User, UserProfile
from utils.serializers import BaseSerializer


class VerifyOtpSerializer(serializers.Serializer):
    otp_token = serializers.CharField(required=True, min_length=8)
    otp = serializers.CharField(required=True, min_length=4)

    def validate(self, data):
        """Validate if a user with this number exists and whether the OTP is
        valid for this user."""
        if data['otp_token']:
            if not User.objects.filter(otp_token=data['otp_token']).exists():
                raise ValidationError(
                    {'error': _('User  doesn\'t exist.')})
            user = User.objects.get(otp_token=data['otp_token'])
            otp = data['otp']
            if not user.is_valid_otp(otp):
                raise ValidationError({"otp": _('Invalid OTP!'), "message": _('Invalid OTP!')})

        return data

    class Meta:
        fields = '__all__'


class OTPLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, min_length=10)

    class Meta:
        fields = '__all__'


class SSOLoginSerializer(serializers.Serializer):
    sso_username = serializers.CharField(required=True, min_length=8)
    sso_payload = serializers.JSONField(required=True)

    def validate(self, data):
        # mobile = data["sso_username"]
        # sso_payload = data["sso_payload"]

        # verified = verify_truecaller_response(mobile, sso_payload)
        # if not verified:
        #     raise ValidationError({'sso_payload': _("Truecaller verification failed.")})

        return data


class UserProfileSerializer(BaseSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"

        extra_kwargs = {
            'user': {'write_only': True},
        }


class UserSerializer(BaseSerializer):
    profile_details = UserProfileSerializer(source='_user_profile', many=False)

    class Meta:
        model = User
        fields = ['phone', 'email', 'is_verified', 'profile_details', 'name']

        extra_kwargs = {
            'company': {'write_only': True},
        }


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'

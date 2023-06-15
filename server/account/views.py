from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from account.methods import UserAuthHelper
from account.models import User, UserProfile
from account.serializers import OTPLoginSerializer, VerifyOtpSerializer, SSOLoginSerializer, LogoutSerializer


# Create your views here.
class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == 'set_password':
            self.permission_classes = [IsAuthenticated]

        return super(AuthViewSet, self).get_permissions()

    @action(
        detail=False,
        methods=["post"],
        serializer_class=OTPLoginSerializer,
        url_path="get-otp", url_name="login",
    )
    def get_otp(self, request, version):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]

        user_instance, created = User.objects.get_or_create(phone=phone)

        if created:
            user_instance.is_app_user = True
            user_instance.save()

        _, otp_token = user_instance.generate_otp()

        data = {
            "otp_token": otp_token,
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=VerifyOtpSerializer,
        url_path="verify-otp", url_name="verify-otp",
    )
    def verify_otp(self, request, version):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_token = serializer.validated_data["otp_token"]

        user_instance = User.objects.get(otp_token=otp_token)

        user_instance.is_verified = True
        user_instance.save()

        data = UserAuthHelper.login_success_response(user_instance, request)
        return Response(data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=SSOLoginSerializer,
        url_path="login/sso", url_name="login",
    )
    def sso_login(self, request, version):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sso_username = serializer.validated_data["sso_username"]
        sso_payload = serializer.validated_data["sso_payload"]

        phone = sso_username[3:]
        user_instance, created = User.objects.get_or_create(phone=phone)

        if created:
            UserProfile.objects.create(
                user=user_instance,
                sso_payload=sso_payload,
                flag_true_caller_signup=True
            )

            user_instance.is_verified = True
            user_instance.save()

        data = UserAuthHelper.login_success_response(user_instance, request)

        return Response(data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=OTPLoginSerializer,
        url_path="check-user", url_name="check-user",
    )
    def check_user(self, request, version):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        is_user_exist = User.objects.filter(phone=phone).exists()
        data = {
            "is_user_exist": is_user_exist,
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=LogoutSerializer,
        url_path="logout", url_name="logout",
    )
    def logout(self, request, version):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserAuthHelper.blacklist_token(
            serializer.validated_data['refresh_token']
        )

        return Response(status=status.HTTP_205_RESET_CONTENT)

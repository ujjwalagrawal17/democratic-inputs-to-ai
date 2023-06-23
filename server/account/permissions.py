from rest_framework.permissions import BasePermission


class IsKycAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user._user_profile.flag_aadhar_card_verified)

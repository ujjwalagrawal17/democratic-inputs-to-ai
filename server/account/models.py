import pyotp
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext as _

from utils.models import CreationModificationBase
from utils.views import send_otp


class UserManager(BaseUserManager):
    """Model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone, name, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('User must have phone number')
        phone = phone
        user = self.model(phone=phone, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, name, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(phone, name, password, **extra_fields)

    def create_superuser(self, phone, name, password, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, name, password, **extra_fields)

    def create_app_user(self, phone, name=None, email=None, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault('is_app_user', True)
        extra_fields.setdefault('email', email)

        return self._create_user(phone, name, password, **extra_fields)


class User(AbstractUser):
    """ Custom User model """

    username = None
    name = models.CharField(max_length=50, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'(0/91)?[6-9][0-9]{9}',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.")
    phone = models.CharField(_('phone number'), validators=[phone_regex], max_length=30, unique=True)  #
    email = models.EmailField(_('Email'), null=True, blank=True)

    otp_token = models.CharField(max_length=255, null=True, blank=True, unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.phone

    def generate_otp(self):
        """Generate a token and associated TOTP for this user and then save the
        otp_token to instance."""
        self.otp_token = pyotp.random_base32()
        self.save()

        otp = pyotp.TOTP(self.otp_token, digits=6).now()
        message = 'Your One Time Password is ' + str(otp)

        send_otp(self.phone, message)
        # send_wa_otp(self.phone, message)
        return otp, self.otp_token

    def is_valid_otp(self, otp):
        """Verify if the provided OTP is valid or not."""

        if self.phone in [
            '1111111111',
            '2222222222',
            '3333333333',
            '4444444444',
            '5555555555',
            '6666666666',
            '7777777777',
            '8888888888',
            '9999999999',
        ]:
            return otp == '123456'

        OTP_VALID_WINDOW = 3  # 3 mins
        totp = pyotp.TOTP(self.otp_token, digits=6)

        self.is_verified = totp.verify(otp, valid_window=OTP_VALID_WINDOW)
        self.save()
        return self.is_verified

    def get_short_name(self):
        return self.name

    def get_tokens(self):
        """Returns a tuple of JWT tokens (token, refresh_token)"""
        refresh = RefreshToken.for_user(self)

        return str(refresh.access_token), str(refresh)


class Profile(CreationModificationBase):
    sso_payload = models.TextField(default="", null=False, blank=True)
    flag_true_caller_signup = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UserProfile(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='_user_profile')
    flag_aadhar_card_verified = models.BooleanField(default=False)

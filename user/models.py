# coding: utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser, \
    AbstractBaseUser, PermissionsMixin, BaseUserManager, \
    UserManager, User
from django.utils.translation import ugettext_lazy as _


class AmazonUserManager(BaseUserManager):
    """Custom UserManager"""

    @classmethod
    def normalize_phone(cls, phone: str):
        phone = ''.join(phone.split(' '))
        phone = ''.join(phone.split('-'))
        return phone

    def _create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not phone:
            raise ValueError('The given username must be set')
        phone = self.normalize_phone(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class AbstractAmazonUser(AbstractBaseUser, PermissionsMixin):
    BASIC = '0'
    PRO = '1'
    TYPE_CHOICE = (
        (BASIC, 'basic'),
        (PRO, 'pro')
    )

    phone = models.CharField(max_length=16, name='phone', db_index=True, unique=True)
    member = models.CharField(max_length=2, choices=TYPE_CHOICE, default=BASIC, name='member')
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    object = AmazonUserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_short_name(self):
        """return a phone"""
        return self.phone

    def get_full_name(self):
        """return a phone"""
        return self.phone


class AmazonUser(AbstractAmazonUser):
    """
    Concrete class of AbstractAmazonUser

    Username, password and email are required. Other fields are optional.
    """

    class Meta(AbstractAmazonUser.Meta):
        swappable = 'AUTH_USER_MODEL'

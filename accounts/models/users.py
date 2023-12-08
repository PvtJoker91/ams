import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group, Permission, AbstractUser, UserManager
from django.db import models
from django.utils import timezone


class AMSGroup(Group):
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class CustomUserManager(BaseUserManager):

    def _create_user(self, first_name, last_name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, first_name=None, last_name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(first_name, last_name, email, password, **extra_fields)

    def create_superuser(self, first_name=None, last_name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(first_name, last_name, email, password, **extra_fields)


class AMSUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True,)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    groups = models.ManyToManyField(AMSGroup, related_name='user', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}' if self.first_name and self.last_name else self.email

    def __str__(self):
        return f'{self.full_name} ({self.pk})'

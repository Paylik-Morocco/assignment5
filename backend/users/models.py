from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email adddress')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.set_password(password)

        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user
    

#Database model for users in the system
class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
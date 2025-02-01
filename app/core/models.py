"""
Database Models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,  # for authentication
    BaseUserManager,  # helps user creation
    PermissionsMixin,  # adds permission-related functionalities
)


class UserManager(BaseUserManager):
    """manager for users"""
    def create_user(self, email, password=None, **extra_field):
        """Create save and retur a new user"""
    # raise valuerror for empty emails
        if not email:
            raise ValueError('User must have an email address.')
    # equivalent to -> user = User(email=email, **extra_field)
    # extra_field any number of keywords
    # arguments dynamically, for flexibility
        user = self.model(email=self.normalize_email(email), **extra_field)
    # not necessary in case of tseting,
    # but sets encrypted password (one way encryption)
        user.set_password(password)
        user.save(using=self._db)  # add multible dbs to project

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Users in system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # default user is active
    # (from permissionmixin class) no regular user should login to admin
    is_staff = models.BooleanField(default=False)

    # for linkage to user model objects = UserManager()
    objects = UserManager()
    USERNAME_FIELD = 'email'  # sets as unique

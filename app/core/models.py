"""
Database Models
"""
import uuid
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,  # for authentication
    BaseUserManager,  # helps user creation
    PermissionsMixin,  # adds permission-related functionalities
)


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    # extracts just the file extension eg .jpg
    ext = os.path.splitext(filename)[1]
    # Generates a new filename using uuid4(). uuid.uuid4()
    # creates a random unique identifier
    filename = f'{uuid.uuid4()}{ext}'
    # Joins 'uploads/recipe/' with the generated filename.
    return os.path.join('uploads', 'recipe', filename)


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


# Model is base class
class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # if user gets deleted also delete recipes
    )
    title = models.CharField(max_length=255)
    # TextField designed to hold more content but not that fast
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    # passing the function reference to dynamically generate a new path
    # each time function is called
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

# string representation of object as titles
    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # if user gets deleted also delete recipes
    )

    # string representation of object as names
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

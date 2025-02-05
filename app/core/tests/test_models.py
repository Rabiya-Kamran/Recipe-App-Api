"""
Tests for models
"""
from decimal import Decimal  # to store values

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


# TestCase so a django unit test
class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful"""
# use @example.com for testing
        email = 'test@example.com'
        password = 'testpass123'
# get_user_model() is a built-in function in Django
# that helps fetch the User model you are using for authentication
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
# check to see if email and passwords are correct
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normaized(self):
        """Test email is normalized for new users"""
        # A list of test cases where the first value is the input email
        # and the second value is the expected normalized emai
        sample_emails = [

            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
# Loops through each test case
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user withot an email rases value error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

# test method used to verify that creating a superuser works correctly
    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',

        )
        # is_superuser and is_staff as true
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

# test method to verify if recipe is being created successfully
    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        # test user to assign to recipe
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description.',
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Testcreating a tag is successful"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

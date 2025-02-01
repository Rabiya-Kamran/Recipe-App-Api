"""
Tests for Django admin modifications
"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


# test case for testing modifications in the Django admin interface.
class AdminSiteTests(TestCase):
    """Tests for django admin. """

# setUp: This is a method that runs before each test
# to prepare the test environment.
    def setUp(self):
        """Create user and client"""
# Client() is a test client
        self.client = Client()
# Creates a superuser for access to admin
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',

        )
        self.client.force_login(self.admin_user)

# Creates a regular user with a name and email
# that will be used in the tests.
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

# test verifies that the Django admin is listing
# the users correctly on the page.
    def test_user_list(self):
        """Test that users are listed on page"""

# Uses reverse to get the URL of the
# core_user_changelist: user lists page
        url = reverse('admin:core_user_changelist')
#  Sends a GET request to the admin user list page to get response.
        res = self.client.get(url)
# Asserts that the response contains the name of the user
# created earlier (in setUp).
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        # self.user.id is the ID of the user that we want to edit,
        # and it’s passed as an argument to generate the correct
        # URL for that user's edit page
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

# checks that  that the page loaded successfully.
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works"""
        # generates the URL for the create new user page
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

"""
Test for user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework.test import APIClient
from rest_framework import status

# app_name = 'user' from urls
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


# public tests- unauthenticated user (dont require authentication)
class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

# setUp() runs before each test.
# initializes APIClient(), which allows us to
# send HTTP requests in the test.
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        # Defines user details to send in the API request.
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',

        }
        # Sends a POST request to create a new user.
        res = self.client.post(CREATE_USER_URL, payload)
        # Checks if the API returns 201 CREATED,
        # meaning the user was successfully created.
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Fetches the created user from the database.
        user = get_user_model().objects.get(email=payload['email'])
        # Verifies that the password is stored correctly.
        self.assertTrue(user.check_password(payload['password']))
        # Ensures the password not  in the API response for security.
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error return if user with email exists"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # test for minimal length of password
    def test_password_too_short_error(self):
        """Test an error is returned if password is too short"""
        payload = {
            'email': 'test@example.com',
            'password': '12',
            'name': 'Test Name',
        }
        # Sends a POST request to create a new user.
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # Looks in the database for a user with this email.
        # exists() returns True if a user is found, False if not.
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials"""
        user_details = {
            'name': 'Test Name',
            'email': 'test2@example.com',
            'password': 'test-pwd',
        }
        # create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        # POSTS TOKEN TO TOKEN URL
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        # check if res.data includes token
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid"""
        create_user(email='test@example.com', password='goodpass')
        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""


# setUp() runs before each test.
# initializes APIClient(), which allows us to
# send HTTP requests in the test.
    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
# Sets up an API client to send HTTP requests.
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        # ME_URL contains details of current authenticated user
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Verifies that the returned data matches the user’s details
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

# It prevents users from creating a new profile via this endpoint
    def test_most_me_not_allowed(self):
        """Test POST is not allowed for me endpoint"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

# ensures that users can update their own profile information securely
    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user"""
        payload = {'name': 'Updated name', 'password': 'newpass123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

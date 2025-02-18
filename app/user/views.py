"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken


from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,

)


# CreateAPIView handles http post request des
class CreateUserView(generics.CreateAPIView):
    """Create a new user in system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    # print("hitttttttttttttttttt")
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user while printing tokens."""

        return self.request.user

"""
Views for the user API
"""
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
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
    # renderer_classes = [JSONRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
            )
        print(request)
        serializer.is_valid(raise_exception=True)  # Handles validation
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    # print("hitttttttttttttttttt")
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user while printing tokens."""
        print("33333333333333")
        return self.request.user

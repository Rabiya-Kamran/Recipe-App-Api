"""
Views for recipe APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


# ModelViewSet is set up to specifically work for models
# (CRUD: it automatically gets API endpoints)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
# RecipeDetailSerializer to get details of recipes by ids to update or create
    serializer_class = serializers.RecipeDetailSerializer
# to specify which model to work with we have to specify queryset
    queryset = Recipe.objects.all()
# users need to authenticate using a token
# How the user authenticates (via token)
    authentication_classes = [TokenAuthentication]
# only authenticated users can access the API
    permission_classes = [IsAuthenticated]

# Overrides get_queryset so that each user sees only their own recipes
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for requests."""
        # if action is list then call RecipeSerializer
        # else call RecipeDetailSerializer
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

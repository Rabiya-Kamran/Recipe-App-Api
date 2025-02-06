"""
Views for recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
    )
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
    )
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
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

# The URL for this action will be: /api/recipes/{id}/upload_image/
# where {id} is the recipe’s ID.
    @action(methods=['POST'], detail=True, url_path='upload_image')
    def upload_image(self, request, pk=None):
        """Uplod an image to recipe"""
# fetches the recipe instance with the given pk (passed in the URL).
        recipe = self.get_object()
# Uses a serializer to validate and process the uploaded image.
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ListModelMixin allows to add mixin functionality
# (CRUD: it automatically gets API endpoints)
# GenericViewSet should be the last thing in definitions
class BaseRecipeAttrViewSet(
                mixins.DestroyModelMixin,
                mixins.UpdateModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """Base viewset for recipe attributes"""
# users need to authenticate using a token
# How the user authenticates (via token)
    authentication_classes = [TokenAuthentication]
# only authenticated users can access the API
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in db"""
    serializer_class = serializers.TagSerializer
# to specify which model to work with we have to specify queryset
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

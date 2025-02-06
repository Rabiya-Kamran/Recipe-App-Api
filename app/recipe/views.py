"""
Views for recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
    )
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
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


# extend_schema_view allows us to extend auto-generated schema
# by djangorest spectacular
# Swagger will show tags and ingredients as available query parameters
@extend_schema_view(
    # to extend schema for list endpoint
    list=extend_schema(
        # This tells Swagger/OpenAPI:
        # The tags and ingredients query parameters exist.
        # They expect strings (comma-separated numbers like "1,2,3") (STR).
        # What they do (filter results based on IDs).
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter.',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            ),
        ],
    ),
)
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

    def _params_to_ints(self, qs):
        """Convert a list of integers."""
        return [int(str_id) for str_id in qs.split(',')]

# Overrides get_queryset so that each user sees only their own recipes
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
# This checks if the user added tags or ingredients in the URL
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
# self.queryset contains all recipes in the database.
        queryset = self.queryset
# _params_to_ints converts a comma-separated string into a list of integers
        if tags:
            tag_ids = self._params_to_ints(tags)
# tags__id__in is a Django ORM filter lookup expression
# used to filter records based on a list of tag IDs
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)
# Filters the results so that only recipes
# created by the logged-in user are returned
        return queryset.filter(
            user=self.request.user
                               ).order_by('-id').distinct()

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


# extend_schema(): to add more details about how the list of tags will work.
# Parameters are like filters that users can add to their request
# OpenApiTypes.INT tells Django that the parameter should be an integer.
# enum restricts the values of assigned_only to 0 or 1
# short description of the parameter that helps users understand what it does
@extend_schema_view(
        list=extend_schema(
            parameters=[
                OpenApiParameter(
                    'assigned_only',
                    OpenApiTypes.INT,
                    enum=[0, 1],
                    description='Filter by items assigned to recipes.',
                ),
            ],
        ),
)
# (CRUD: it automatically gets API endpoints)
# ListModelMixin allows to add mixin functionality
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
# method checks if the URL has a query parameter called assigned_only
# If assigned_only=1 is present in the URL,
# it turns the value into True (we want to filter tags assigned to recipes)
# If no parameter is provided (or if it's assigned_only=0),
# it turns into False (meaning show all tags).
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
# grabs the default list of tags from the database
        queryset = self.queryset
# Only include tags that are assigned to a recipe.
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)
# filters the tags to only show those that belong
# to the currently logged-in user.
        return queryset.filter(
            user=self.request.user
            ).order_by('-name').distinct()


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in db"""
    serializer_class = serializers.TagSerializer
# to specify which model to work with we have to specify queryset
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

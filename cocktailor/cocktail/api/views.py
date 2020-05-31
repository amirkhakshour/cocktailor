from rest_framework import viewsets
from cocktail.models import Cocktail, Ingredient, AvailableIngredient
from .serializers import (
    IngredientSerializer,
    CocktailBaseSerializer,
    AvailableIngredientSerializer,
)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CocktailViewSet(viewsets.ModelViewSet):
    queryset = Cocktail.objects.all()
    serializer_class = CocktailBaseSerializer


class AvailableIngredientViewSet(viewsets.ModelViewSet):
    queryset = AvailableIngredient.objects.all()
    serializer_class = AvailableIngredientSerializer

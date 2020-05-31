from rest_framework import viewsets
from cocktail.models import Cocktail, Ingredient
from .serializers import IngredientSerializer, CocktailBaseSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CocktailViewSet(viewsets.ModelViewSet):
    queryset = Cocktail.objects.all()
    serializer_class = CocktailBaseSerializer

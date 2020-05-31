from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=False, methods=["get"])
    def cocktails(self, request, **kwargs):
        """Return list of cocktails that can be made using available
        ingredients which are not expired yet."""
        fresh_ingredients = AvailableIngredient.objects.fresh()
        cocktails = Cocktail.objects.includes_ingredients(
            [item.ingredient for item in fresh_ingredients]
        )
        serializer = CocktailBaseSerializer(cocktails, many=True)
        return Response(serializer.data)

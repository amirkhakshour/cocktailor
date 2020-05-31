from rest_framework import serializers

from cocktail.models import Ingredient, Cocktail


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class CocktailSerializer(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all()
    )

    class Meta:
        model = Cocktail
        fields = "__all__"


class CocktailBaseSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Cocktail
        fields = "__all__"

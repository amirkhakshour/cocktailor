import random
from datetime import timedelta
from django.utils import timezone
from rest_framework import status

from cocktail.models import AvailableIngredient
from cocktail.api.serializers import AvailableIngredientSerializer
from .factories import IngredientFactory, CocktailFactory


# Note: testing other endpoints for Ingredient, Cocktail
#   is useless since they have no business logic inside and
#   the functionality has been already covered by DRF, django tests.


def test_available_ingredients_invalid_expire_date(db, user_api_client):
    avail_ingred = AvailableIngredient.objects.create(
        ingredient=IngredientFactory(), expire_date=timezone.now() + timedelta(days=1)
    )

    past_time = timezone.now() - timedelta(days=1)
    avail_ingred.expire_date = past_time
    serializer = AvailableIngredientSerializer(avail_ingred)
    resp = user_api_client.api_call(
        "api:api_cocktails:availableingredient-list", "post", data=serializer.data
    )
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    errors = resp.json()
    assert "expire_date" in errors
    assert "must be in the future time" in errors["expire_date"][0]


def test_cocktails_for_available_ingreds(db, user_api_client):
    num_ingredients = 6
    num_cocktails = 20
    ingredients = [IngredientFactory() for _ in range(num_ingredients)]
    for item in range(num_cocktails):
        CocktailFactory.create(
            ingredients=random.sample(ingredients, random.randint(3, num_ingredients))
        )

    resp = user_api_client.api_call(
        "api:api_cocktails:availableingredient-cocktails", "get"
    )
    assert resp.status_code == status.HTTP_200_OK


def test_cocktails_for_some_ingreds(db, user_api_client):
    """
    You get the idea:
    - Create some cocktails,
    - Add two AvailableIngredient based on ingredients on those cocktails
    - Check if the returned number of cocktails from `api:api_cocktails:availableingredient-cocktails` equals
        to the ones that contains at least one of the available ingredients
    """
    pass


def test_cocktails_for_all_ingreds(db, user_api_client):
    """
    Note:
    - For first run it must be failed!
    - Then we refactor AvailableIngredientViewSet.cocktails to check for a keyword in `kwargs`
        if this keyword is passed by user, then use `includes_only_ingredients` instead of `includes_any_ingredients`

    You get the idea:
    - Create some cocktails
    - Add two AvailableIngredient based on ingredients on those cocktails
    - Check if the returned number of cocktails from `api:api_cocktails:availableingredient-cocktails` equals
        to the ones that contains all the available ingredients (I'd write a nested loop to calculate
        number of cocktails that contain all our available cocktails and test it agains the number
        of items returned by endpoint)
    """
    pass

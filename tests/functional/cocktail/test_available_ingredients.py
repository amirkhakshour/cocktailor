from datetime import timedelta
from django.utils import timezone
from rest_framework import status

from cocktail.models import AvailableIngredient
from cocktail.api.serializers import AvailableIngredientSerializer
from .factories import IngredientFactory


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

import requests
import logging

from django.db.models import Q
from django.core.management.base import BaseCommand
from django.conf import settings

from cocktail.models import Ingredient, Cocktail
from cocktail.api.serializers import IngredientSerializer, CocktailSerializer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Initialize cocktail Cocktail and Ingredient models from external API."

    def handle(self, *args, **options):
        if Ingredient.objects.count() == 0:
            logger.info("Importing Ingredients ...")
            response = requests.get(settings.COCKTAIL_INIT_INGREDIENTS_URL)
            serializer = IngredientSerializer(data=response.json(), many=True)
            if serializer.is_valid(True):
                imported = serializer.save()
                logger.info(f"Imported {len(imported)} ingredients!")

        if Cocktail.objects.count() == 0:
            logger.info("Importing Cocktails ...")
            response = requests.get(settings.COCKTAIL_INIT_COCKTAILS_URL)
            cocktails = response.json()
            valid_cocktails = []
            for cid, cocktail in enumerate(cocktails):
                ingreds_list = cocktail["ingredients"]
                q = Q()
                for ingred in ingreds_list:
                    q = q | Q(
                        name__iexact=ingred
                    )  # instead of case sensitive __in query

                ingreds = Ingredient.objects.filter(q)
                if len(ingreds) != len(ingreds_list):
                    diff = set([i.name for i in ingreds]) - set(ingreds_list)
                    logger.error(f"Ingredient not found: {diff}")
                else:
                    cocktails[cid]["ingredients"] = [i.pk for i in ingreds]
                    valid_cocktails.append(cocktails[cid])
            serializer = CocktailSerializer(data=valid_cocktails, many=True)
            if serializer.is_valid(True):
                imported = serializer.save()
                logger.info(f"Imported {len(imported)} cocktails!")

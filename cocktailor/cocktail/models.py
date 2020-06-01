from typing import List

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import date as date_filter


def validate_future_dt(dt):
    """Check if given date time is greater than now!."""
    if dt <= timezone.now():
        raise ValidationError(
            _("%(value)s must be in the future time!"),
            params={"value": date_filter(dt, settings.DATETIME_FORMAT)},
        )


class Ingredient(models.Model):
    """Describes an ingredient for cocktail."""

    name = models.CharField(max_length=255, unique=True)
    alcoholic = models.BooleanField()

    def __str__(self):
        return self.name


class AvailableIngredientQuerySet(models.QuerySet):
    def fresh(self):
        return self.filter(models.Q(expire_date__gt=timezone.now()),)


class AvailableIngredient(models.Model):
    """Describes an ingredient for cocktail. This ingredient contains attributes like
    expiration date and type of drink, weather it's alcoholic or not."""

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    expire_date = models.DateTimeField(
        _("expire date"), db_index=True, validators=[validate_future_dt]
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = AvailableIngredientQuerySet.as_manager()

    def __str__(self):
        date_format = settings.DATETIME_FORMAT
        return "AvailableIngredient %s  expire_date=%s " % (
            self.ingredient,
            date_filter(self.expire_date, date_format),
        )

    class Meta:
        ordering = ("-modified", "-created", "-expire_date")


class CocktailQuerySet(models.QuerySet):
    def includes_any_ingredients(self, ingredients: List[Ingredient]):
        """Manager Method that returns any cocktail that contains at least one ingredient in the list."""
        return self.filter(ingredients__in=ingredients)

    def includes_only_ingredients(self, ingredients: List[Ingredient]):
        """Manager Method that returns only cocktails that contain all the ingredient in the list."""
        cids = Cocktail.objects.filter(ingredients__in=ingredients).values_list(
            "id", flat=True
        )
        return (
            self.filter(id__in=cids)
            .annotate(num_ingreds=Count("ingredients"))
            .filter(num_ingreds=len(ingredients))
        )


class Cocktail(models.Model):
    """Basic object representing a Cocktail which includes different ingredients."""

    name = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = CocktailQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-modified", "-created")

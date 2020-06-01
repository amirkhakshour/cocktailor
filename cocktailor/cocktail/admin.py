from django.contrib import admin
from .models import Cocktail, Ingredient, AvailableIngredient

admin.site.register(Ingredient)
admin.site.register(AvailableIngredient)
admin.site.register(Cocktail)

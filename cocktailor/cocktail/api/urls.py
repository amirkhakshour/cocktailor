from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import IngredientViewSet, CocktailViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api_cocktails"
router.register("ingredients", IngredientViewSet)
router.register("cocktails", CocktailViewSet)

urlpatterns = router.urls

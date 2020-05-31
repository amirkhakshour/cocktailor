import factory
from cocktail.models import Ingredient, Cocktail


class IngredientFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Ingredient %03d" % n)
    alcoholic = factory.Faker("boolean")

    class Meta:
        model = Ingredient


class CocktailFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Cocktail %03d" % n)

    class Meta:
        model = Cocktail

    @factory.post_generation
    def ingredients(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for ingredient in extracted:
                self.ingredients.add(ingredient)

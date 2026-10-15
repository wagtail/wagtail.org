import factory

from wagtailio.taxonomy.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Category {n}")

    class Meta:
        model = Category

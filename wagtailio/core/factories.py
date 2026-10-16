import factory
import wagtail_factories

from wagtailio.core.models import ContentPage, HomePage


class HomePageFactory(wagtail_factories.PageFactory):
    title = factory.Sequence(lambda n: f"Home page {n}")

    class Meta:
        model = HomePage


class ContentPageFactory(wagtail_factories.PageFactory):
    title = factory.Sequence(lambda n: f"Content page {n}")

    class Meta:
        model = ContentPage

from django.conf import settings
from django.db import transaction

from wagtailio.roadmap import github
from wagtailio.roadmap.github import RoadmapSyncError
from wagtailio.roadmap.models import Milestone, MilestoneItem


__all__ = ["MissingTokenError", "RoadmapSyncError", "apply", "process"]


class MissingTokenError(RoadmapSyncError):
    pass


def apply(milestones: list[github.Milestone]):
    """
    Update the roadmap milestones and items in the database to match the given
    milestones from GitHub.

    Items are matched by their GitHub issue number, so an item that has moved to
    another milestone keeps its call to action URL and sort order. Items that are
    no longer in any of the given milestones are deleted.

    Returns a summary dict with the number of milestones and items synchronised,
    and the number of stale items deleted.
    """
    seen_milestone_numbers = set()
    seen_item_numbers = set()

    with transaction.atomic():
        for data in milestones:
            milestone, _ = Milestone.objects.update_or_create(
                number=data.number,
                defaults=data.model_dump(exclude={"items"}),
            )
            seen_milestone_numbers.add(data.number)

            for item_data in data.items:
                item = MilestoneItem.objects.filter(number=item_data.number).first()
                if not item:
                    item = MilestoneItem(number=item_data.number)
                seen_item_numbers.add(item_data.number)

                for field, value in item_data.model_dump().items():
                    setattr(item, field, value)
                item.milestone = milestone
                item.full_clean()
                item.save()

        # Remove items that are no longer attached to the seen milestones.
        deleted_items, _ = (
            MilestoneItem.objects.filter(milestone__number__in=seen_milestone_numbers)
            .exclude(number__in=seen_item_numbers)
            .delete()
        )

    return {
        "milestones": len(seen_milestone_numbers),
        "items": len(seen_item_numbers),
        "deleted_items": deleted_items,
    }


def process(token=""):
    """Synchronise roadmap milestones and items from GitHub."""
    token = token or settings.GITHUB_ROADMAP_ACCESS_TOKEN
    if not token:
        raise MissingTokenError("No GitHub access token supplied or configured.")

    return apply(github.fetch(token))

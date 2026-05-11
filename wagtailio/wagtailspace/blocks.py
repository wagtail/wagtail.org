from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from wagtailio.core.blocks import CTALinkMixin, RichTextBlock, VideoBlock


class SpaceDropdownItemValue(blocks.StructValue):
    @property
    def cta_resolved_url(self):
        if url := self.get("cta_url"):
            return url
        if page := self.get("cta_page"):
            return page.url
        return ""


class SpaceTextBlock(RichTextBlock):
    class Meta:
        template = "patterns/components/streamfields/space_text_block.html"
        label = "Text"


class CenteredSpaceTextBlock(RichTextBlock):
    class Meta:
        template = "patterns/components/streamfields/centered_space_text_block.html"
        icon = "title"
        label = "Centered Text"


class SpaceCTABlock(CTALinkMixin):
    text = blocks.CharBlock(label="CTA text", max_length=255, required=False)
    cta_page = blocks.PageChooserBlock(label="CTA page", required=False)
    cta_url = blocks.URLBlock(label="CTA URL", required=False)

    class Meta:
        icon = "bullhorn"
        template = "patterns/components/streamfields/cta/cta_space.html"
        label = "CTA"


class SpeakerBlock(blocks.StructBlock):
    speaker_image = ImageBlock(
        required=True, help_text="Use a square image for best results."
    )
    speaker_name = blocks.CharBlock(max_length=255, required=True)
    speaker_talk = blocks.TextBlock(max_length=255, required=False)
    speaker_url = blocks.URLBlock(
        label="Talk URL",
        required=False,
        help_text="Optional link for talk description.",
    )

    class Meta:
        template = "patterns/components/streamfields/speaker_block/speaker_block.html"


class SpeakerHighlightBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255, required=False)
    speaker = blocks.ListBlock(SpeakerBlock())

    class Meta:
        icon = "group"
        template = (
            "patterns/components/streamfields/speaker_highlight/speaker_highlight.html"
        )
        label = "Speaker Highlight"


class SponsorLogoBlock(blocks.StructBlock):
    sponsor_logo = ImageBlock(required=True)
    sponsor_link = blocks.URLBlock(label="Sponsor Link", required=True)

    class Meta:
        template = (
            "patterns/components/streamfields/sponsor_logo/sponsorlogo_block.html"
        )


class SponsorBlock(blocks.StructBlock):
    sponsor_type = blocks.CharBlock(max_length=255, required=True)
    sponsors = blocks.ListBlock(SponsorLogoBlock())

    class Meta:
        template = "patterns/components/streamfields/sponsor_block/sponsor_block.html"


class SponsorHighlightBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255, required=False)
    sponsor = blocks.StreamBlock([("sponsor", SponsorBlock())], blank=True)

    class Meta:
        icon = "pick"
        template = (
            "patterns/components/streamfields/sponsor_highlight/sponsor_highlight.html"
        )
        label = "Sponsor Highlight"


class SpaceExtendedCTABlock(CTALinkMixin):
    heading = blocks.CharBlock(label="Heading", max_length=255)
    description = blocks.TextBlock(label="Description")
    text = blocks.CharBlock(label="CTA text", max_length=255, required=False)
    cta_page = blocks.PageChooserBlock(label="CTA page", required=False)
    cta_url = blocks.URLBlock(label="CTA URL", required=False)

    class Meta:
        icon = "bullhorn"
        template = "patterns/components/streamfields/space_extended_cta/space_extended_cta_block.html"
        label = "Extended CTA"


class SpaceDropdownItemBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    text = blocks.TextBlock(required=False)
    cta_text = blocks.CharBlock(label="CTA text", max_length=255, required=False)
    cta_page = blocks.PageChooserBlock(label="CTA page", required=False)
    cta_url = blocks.URLBlock(label="CTA URL", required=False)

    class Meta:
        icon = "collapse-down"
        label = "Dropdown item"
        value_class = SpaceDropdownItemValue


class SpaceDropdownBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255, required=False)
    items = blocks.ListBlock(SpaceDropdownItemBlock())

    class Meta:
        icon = "list-ul"
        template = "patterns/components/streamfields/space_dropdown_block/space_dropdown_block.html"
        label = "Dropdown"


class SpaceVideoBlock(VideoBlock):
    class Meta:
        icon = "media"
        template = (
            "patterns/components/streamfields/space_video_block/space_video_block.html"
        )
        label = "Video"


class SpaceStoryBlock(blocks.StreamBlock):
    rich_text = SpaceTextBlock()
    centered_text = CenteredSpaceTextBlock()
    image = ImageBlock(required=False)
    cta_button = SpaceCTABlock()
    extended_cta = SpaceExtendedCTABlock()
    video = SpaceVideoBlock()
    speaker_highlight = SpeakerHighlightBlock()
    sponsor_highlight = SponsorHighlightBlock()
    dropdown = SpaceDropdownBlock()

    class Meta:
        template = "patterns/components/streamfields/space_story_block.html"


# --------------- Wagtail Space Navigation ---------------


class SpaceMenuSectionBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=255)
    space_menu_page = blocks.PageChooserBlock(label="Page", required=False)
    space_menu_url = blocks.URLBlock(label="External Link", required=False)

    class Meta:
        icon = "bars"
        label = "Space menu section"

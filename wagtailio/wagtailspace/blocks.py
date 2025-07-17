from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from wagtailio.core.blocks import CTALinkMixin, RichTextBlock


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

    class Meta:
        template = "patterns/components/streamfields/speaker_block/speaker_block.html"


class SpeakerHighlightBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255, required=False)
    speaker = blocks.StreamBlock([("speaker", SpeakerBlock())], blank=True, max_num=4)

    class Meta:
        icon = "group"
        template = (
            "patterns/components/streamfields/speaker_highlight/speaker_highlight.html"
        )
        label = "Speaker Highlight"


class SponsorBlock(blocks.StructBlock):
    sponsor_type = blocks.CharBlock(max_length=255, required=True)
    sponsor_logo = blocks.ListBlock(ImageBlock())

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


class SpaceStoryBlock(blocks.StreamBlock):
    rich_text = SpaceTextBlock()
    centered_text = CenteredSpaceTextBlock()
    image = ImageBlock(required=False)
    cta_button = SpaceCTABlock()
    speaker_highlight = SpeakerHighlightBlock()
    sponsor_highlight = SponsorHighlightBlock()

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

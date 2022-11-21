from wagtailio.core.blocks import StandaloneCTABlock
from wagtailio.utils.blocks import StoryBlock
from wagtailio.core.blocks import TeaserBlock, HighlightBlock
from wagtail.snippets.blocks import SnippetChooserBlock




class BlogStoryBlock(StoryBlock):
    standalone_cta = StandaloneCTABlock()
    get_started_block = SnippetChooserBlock(
        "core.GetStartedSnippet",
        icon="th-list",
        template="patterns/components/streamfields/get_started_block/get_started_block.html",
    )
    sign_up_form = SnippetChooserBlock(
        "core.SignupFormSnippet",
        icon="envelope-open-text",
        template="patterns/components/streamfields/sign_up_form_block/sign_up_form_block.html",
    )
    highlight = HighlightBlock()
    teaser = TeaserBlock()

from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = "wagtailio.images"
    default_auto_field = "django.db.models.AutoField"
    ready_is_done = False

    def ready(self):
        if not self.ready_is_done:
            # Load the patch that adds default_alt_text to ImageBlock
            from . import image_block_patch  # noqa

            self.ready_is_done = True
        else:
            print(
                "{}.ready() executed more than once! This method's code is skipped on subsequent runs.".format(
                    self.__class__.__name__
                )
            )

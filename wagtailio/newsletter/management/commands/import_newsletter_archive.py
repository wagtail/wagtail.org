from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


ARCHIVE_URLS = {
    "137": "http://eepurl.com/ivTG6c",
    "138": "http://eepurl.com/iwZ7G6",
    "139": "http://eepurl.com/ixNV4w",
    "140": "http://eepurl.com/iyhGYM",
    "141": "http://eepurl.com/iyLQJc",
    "142": "http://eepurl.com/iz9nMQ",
    "143": "http://eepurl.com/iA6xHw",
    "144": "http://eepurl.com/iB42Jg",
    "145": "http://eepurl.com/iC0wWc",
    "146": "http://eepurl.com/iDy-C6",
    "147": "http://eepurl.com/iD5k_E",
    "148": "http://eepurl.com/iE1QSQ",
    "149": "http://eepurl.com/iF-z82",
    "150": "http://eepurl.com/iHNgmU",
    "151": "http://eepurl.com/iIIKyA",
    "152": "http://eepurl.com/iJFzbY",
    "153": "http://eepurl.com/iKHkas",
    "154": "http://eepurl.com/iLyeCs",
    "155": "http://eepurl.com/iMuT3E",
    "156": "http://eepurl.com/iNnQKE",
    "157": "http://eepurl.com/iOc4L2",
    "158": "http://eepurl.com/iPcRkw",
    "159": "http://eepurl.com/iP2mTE",
    "160": "http://eepurl.com/iQW_y2",
    "161": "http://eepurl.com/iRVoYw",
    "162": "http://eepurl.com/iSHTWI",
    "164": "http://eepurl.com/iTA9b-",
    "165": "http://eepurl.com/iUnY6Y",
    "166": "http://eepurl.com/iWD_hE",
    "167": "http://eepurl.com/iXooRM",
    "168": "http://eepurl.com/iYlhYU",
    "169": "http://eepurl.com/iYMLro",
    "170": "http://eepurl.com/i0FTI2",
    "171": "http://eepurl.com/i0GS8s",
    "172": "http://eepurl.com/i1BZRU",
    "173": "http://eepurl.com/i2KzkE",
    "174": "http://eepurl.com/i367AI",
    "175": "http://eepurl.com/i4ZGe6",
    "176": "http://eepurl.com/i53IVA",
    "177": "http://eepurl.com/i7ouKk",
    "178": "http://eepurl.com/i8devU",
    "179": "http://eepurl.com/i87DBY",
    "180": "http://eepurl.com/i-gM12",
    "181": "http://eepurl.com/i_rL9Y",
    "182": "http://eepurl.com/jarS22",
    "183": "http://eepurl.com/jbyaXQ",
    "184": "http://eepurl.com/jcHhc6",
    "185": "http://eepurl.com/jdEVZo",
    "186": "http://eepurl.com/jepIFY",
    "187": "http://eepurl.com/jeIw_Y",
    "188": "https://mailchi.mp/wagtail/twiw-11036059",
    "189": "https://mailchi.mp/wagtail/twiw-11036356",
    "190": "https://mailchi.mp/wagtail/twiw-11036662",
    "191": "https://mailchi.mp/wagtail/twiw-11036961",
    "192": "https://mailchi.mp/wagtail/twiw-11037103",
    "193": "https://mailchi.mp/wagtail/twiw-11037192",
    "194": "https://mailchi.mp/wagtail/twiw-11037409",
    "195": "https://mailchi.mp/wagtail/twiw-11037646",
    "196": "https://mailchi.mp/wagtail/twiw-11037909",
    "197": "https://mailchi.mp/wagtail/twiw-11038051",
    "198": "https://mailchi.mp/wagtail/twiw-11038440",
    "199": "https://mailchi.mp/wagtail/twiw-11038881",
    "200": "https://mailchi.mp/wagtail/twiw-11039169",
    "201": "https://mailchi.mp/wagtail/twiw-11039409",
    "202": "https://mailchi.mp/wagtail/twiw-11039835",
    "203": "https://mailchi.mp/wagtail/twiw-11040202",
    "204": "https://mailchi.mp/wagtail/twiw-11040423",
    "205": "https://mailchi.mp/wagtail/twiw-11040654",
    "206": "https://mailchi.mp/wagtail/twiw-11040908",
    "207": "https://mailchi.mp/wagtail/twiw-11041194",
    "208": "https://mailchi.mp/wagtail/twiw-11041498",
    "209": "https://mailchi.mp/wagtail/twiw-11041706",
    "210": "https://mailchi.mp/wagtail/twiw-11041967",
    "211": "https://mailchi.mp/wagtail/twiw-11042082",
    "212": "https://mailchi.mp/wagtail/twiw-11042473",
    "213": "https://mailchi.mp/wagtail/twiw-11042689",
    "214": "https://mailchi.mp/wagtail/twiw-11042944",
    "215": "https://mailchi.mp/wagtail/twiw-11043202",
    "216": "https://mailchi.mp/wagtail/twiw-11043559",
    "217": "https://mailchi.mp/wagtail/twiw-11043971",
}


class Command(BaseCommand):
    help = "Import all archived newsletters"

    def handle(self, *args, **options):
        failures = []
        for issue_num, url in ARCHIVE_URLS.items():
            title = f"Issue #{issue_num}"
            self.stdout.write(f"Importing {title}...")
            try:
                call_command("import_newsletter", url, title)
            except Exception as error:  # noqa: BLE001 - keep going, report at the end
                self.stderr.write(self.style.ERROR(f"{title} failed: {error}"))
                failures.append(title)
            else:
                self.stdout.write(self.style.SUCCESS(f"Successfully imported {title}"))

        if failures:
            raise CommandError(f"{len(failures)} issues failed: {', '.join(failures)}")

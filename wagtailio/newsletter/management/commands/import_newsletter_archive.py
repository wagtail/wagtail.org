from django.core.management import call_command
from django.core.management.base import BaseCommand


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
}


class Command(BaseCommand):
    help = "Import all archived newsletters"

    def handle(self, *args, **options):
        for issue_num, url in ARCHIVE_URLS.items():
            title = f"Issue #{issue_num}"
            self.stdout.write(f"Importing {title}...")
            call_command("import_newsletter", url, title)
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {title}"))

from django.utils.translation import ugettext_lazy as _
from django.db import models


ORDER_STATUS = (
    (0, "Pending"),
    (1, "In Progress"),
    (2, "Delivered")
)

UNIT_CHOICES = (
    ("kg", _("Kilograms")),
    ("gm", _("Grams")),
    ("units", _("Units")),
    ("dz", _("Dozen")),
    ("carton", _("Carton")),
    ("ltr", _("Litres")),
    ("ml", _("Mili Litres")),
    ("gal", _("Gallons")),
)


CURRENCY_CHOICES = (
    (0.0, "DHS"),
    (1.0, "INR")
)

COUNTRY_CHOICES = (("United Arab Emirates", _('United Arab Emirates')),
                   ("India", _('India'))
                   )
TAX_TYPES = (("TRN", "TRN"), ("GST", "GST"))

VAT_CHOICES = {
    "India": 0.135,
    "United Arab Emirates": 0.05,
}


STATUS_CHOICES = ((0, _("Pending")),
                  (1, _("Confirmed")),
                  (2, _("Item collected")),
                  (3, _("Item processed")),
                  (4, _("Enroute")),
                  (5, _("Delivered"))
                  )

KTM = 'Kathmandu'
LTP = 'Lalitpur'
BKT = 'Bhaktapur'

CITY_CHOICES = ((KTM, _('Kathmandu')),
                (LTP, _('Lalitpur')),
                (BKT, _('Bhaktapur')),
                )

CITY_AREA_DICT = [
    dict(district=KTM, area=['okmandu1', 'youmandu2', 'gomandu3']),
    dict(district=LTP, area=['Lupur1', 'kitpur2', 'palpur3']),
    dict(district=BKT, area=['Baktapur1', 'Bhakur2', 'Bhakr3']),
]

area_choices = list()
i = 0
for district in CITY_AREA_DICT:
    for j, area in enumerate(district['area']):
        area_choices.append(
            ((area + "__" + district['district']), _(area)))  # its is a tuple, its not redundant braces.

area_choices = tuple(area_choices)
# format ['okmandu1__Kathmandu', ...]

ADDRESS_CHOICES = (
    ("villa", _("Villa")),
    ("apartment", _("Apartment")),
    ("work", _("Work"))
)

MODIFIER_CHOICES = (
    ("warranty", _("Warranty")),
    # ("color", _("Color")),
)

MEDIA_CHOICES = (
    ("file", _("file")),
    ("video", _("video link"))
)

TICKET_CHOICES = (
    (0.0, _("Open")),
    (1.0, _("Closed"))
)

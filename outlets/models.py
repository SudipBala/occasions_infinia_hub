from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from libs.fields import SizeRestrictedThumbnailerField


class OfferBannerModel(models.Model):
    banner_image = SizeRestrictedThumbnailerField("Background Image", upload_to="photos/banners/",
                                                  max_upload_size=10485760, resize_source=dict(size=(300, 0),
                                                                                               sharpen=True,
                                                                                               replace_alpha="#fff"
                                                                                               ),
                                                  max_length=500)
    offer_message = models.TextField("Offer Description", blank=True, help_text="Describe your Store.")
    offer_discount = models.TextField("Offer Discount", blank=True, help_text="Discount percentage")

from django.core.validators import MinValueValidator
from django.db import models

from libs.constants import CURRENCY_CHOICES
from libs.models import CustomModel


class DeliveryPolicy(CustomModel):
    outlet = models.ForeignKey("outlets.Outlet", verbose_name="Outlet", on_delete=models.CASCADE)
    radius = models.FloatField("Radius (in km)",unique=True, validators=[
        MinValueValidator(0, "distance is below zero.")
    ])
    price = models.FloatField("Delivery Price", help_text="tentative price", default=0,
                              validators=
                              [MinValueValidator(0, "below minimum price")])
    currency = models.FloatField("Currency", choices=CURRENCY_CHOICES, default=0, max_length=5)
    delivery_time = models.FloatField("Tentative Time to delivery(in hours)",
                                      help_text="it includes 'processing' + 'delivery' time.",
                                      validators=[
                                          MinValueValidator(0, "Value should be over zero."),
                                      ]
                                      )

    def __str__(self):
        return f"Delivery Policy {str(self.id)}"




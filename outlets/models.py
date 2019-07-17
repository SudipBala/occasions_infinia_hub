from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from libs.fields import CustomJsonField
from outlets.outlet_models import Outlet
from outlets.stock_models import OutletStock


class OutletItemLine(models.Model):
    stocked_item = models.ForeignKey(OutletStock, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(_("Count"), default=1, validators=(
        MinValueValidator(0, "min is zero."),
        MaxValueValidator(1000, "max is thousand."),
    ))

    actual_price = models.FloatField(_("Actual price"), default=0,
                                     validators=[MinValueValidator(0, "price cant be negative")])
    discount_amount = models.FloatField(_("Discount percentage"), default=0,
                                        validators=[MinValueValidator(0, "discount cant be negative")])
    net_price = models.FloatField(_("Net Price"), default=0,
                                  validators=[MinValueValidator(0, "price cant be negative")])
    unit_price = models.FloatField(_("Unit Price Marked Price"), null=True)
    unit_selling_price = models.FloatField(_("Unit Selling Price"), null=True)
    stock_sku = models.CharField(_("SKU"), max_length=40, null=True)
    stock_display_name = models.CharField(max_length=250, null=True)

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, **kwargs):
        quantity = kwargs.get('quantity', 1)
        self.quantity = quantity
        self.save()

    def update_quantity(self, **kwargs):
        quantity = kwargs.get('quantity', 1)
        self.quantity += quantity
        self.save()

    def get_total(self):
        return self.get_quantity() * self.stocked_item.price

    def _check_item_quantity(self):
        if self.quantity > self.stocked_item.available:
            raise ValidationError(
                {
                    "available": "Chosen quantity greater than availability , stocked_item {0} {1}".format(
                        self.stocked_item.item.display_name,
                        self.stocked_item.outlet)
                }
            )

    def _check_quantity(self):
        if self.quantity < self.stocked_item.minimum_quantity:
            raise ValidationError({'minimum_quantity': 'You have to buy at least {min_quantity}'.
                                  format(quantity=self.quantity,
                                         min_quantity=self.stocked_item.minimum_quantity)})
        if self.stocked_item.maximum_quantity and self.quantity > self.stocked_item.maximum_quantity:
            raise ValidationError({'maximum_quantity': 'You cannot buy more than {max_quantity} items'.
                                  format(quantity=self.quantity,
                                         max_quantity=self.stocked_item.maximum_quantity)})

    def clean(self):
        self._check_item_quantity()
        self._check_quantity()

    def __str__(self):
        return "{quantity} {name} (SKU:{sku})".format(name=self.stocked_item.item.display_name,
                                                      sku=self.stocked_item.sku,
                                                      quantity=self.quantity
                                                      )

    def save(self, commit=False, *args, **kwargs):
        self.clean()
        if not self.id:
            self.unit_price = self.stocked_item.price
            self.unit_selling_price = self.stocked_item.price
            self.stock_sku = self.stocked_item.sku
            self.quantity = self.quantity
            self.stock_display_name = self.stocked_item.get_item_name()

        if self.id and not commit:
            raise ValidationError("Can't be saved again.")
        super(OutletItemLine, self).save(*args, **kwargs)


class OutletCart(models.Model):
    associated_outlet = models.ForeignKey(Outlet, on_delete=models.DO_NOTHING)
    itemline = models.ManyToManyField(OutletItemLine)
    associated_user = models.IntegerField(blank=True, null=True)
    checked_out = models.BooleanField(default=False)

    def __str__(self):
        return "cart %s" % (str(self.id))


class OutletInvoice(models.Model):
    invoice_number = models.CharField("Invoice Number", max_length=16)
    associated_cart = models.ForeignKey(OutletCart, null=True, on_delete=models.SET_NULL)
    associated_outlet = models.ForeignKey(Outlet, null=True, on_delete=models.SET_NULL)
    # itemline_data = models.ManyToManyField(OutletItemLine, blank=True)
    subtotal = models.FloatField(_("Sub Total"), default=0,
                                 validators=[MinValueValidator(0, "price cant be negative")])
    additional_discount = models.FloatField(_("discount on cart"), default=0,
                                            validators=[MinValueValidator(0, "discount cant be negative")], )
    shipping_cost = CustomJsonField(_("Shipping Cost"), null=True, blank=True, default={})

    vat = models.FloatField(_("VAT"), default=0.13,
                            validators=[MinValueValidator(0, "vat cant be negative")], )

    errors = models.CharField(_("Reasons"), max_length=500, default="")

    grand_total = models.FloatField(_("Grand Total"), default=0.13, validators=[
        MinValueValidator(0, "Grand Total cant be negative")
    ])

    @property
    def vat(self):
        # vat choices for uae/india
        return 0

    @property
    def total(self):
        # returns subtotal minus shipping cost
        return round(self.subtotal-self.get_shipping_cost().get('price', 0), 2)

    def get_shipping_cost(self):
        #get shipping cost
        return {}

    def add_shipping_cost_to_subtotal(self):
        if hasattr(self, '_added'):
            return
        self.subtotal += self.get_shipping_cost().get('price', 0)
        self._added = True

    def get_vat_amount(self):
        return round((self.subtotal - self.additional_discount) * self.vat, 2)

    def get_total_with_shipping_amount(self):
        return round(self.subtotal - self.additional_discount, 2)

    def get_grand_total(self):
        return round((self.subtotal - self.additional_discount) * (1 + self.vat), 2)

    @property
    def get_grand_total_without_vat(self):
        return round((self.subtotal - self.additional_discount), 2)

    def get_grand_total_with_shipping_and_vat(self):
        return round((self.subtotal - self.additional_discount) * (1 + self.vat), 2)

    def __str__(self):
        return "Invoice %s" % self.id

    def get_display_for_template(self):
        return ', '.join([str(il_data.itemline) for il_data in self.associated_cart.itemline.all()])

    def _clean_itemline_data(self):
        if not len(set(self.associated_cart.itemline.values_list('itemline__stocked_item__store', flat=True))) == 1:
            raise ValidationError({"itemline_data": "itemlines dont belong to same store."})

    def save(self, commit=False, *args, **kwargs):
        if self.id:
            self._clean_itemline_data()
        self.grand_total = self.get_grand_total_with_shipping_and_vat()
        self.shipping_cost = self.get_shipping_cost()

        if self.id and not commit:
            raise ValidationError("Can't be saved again.")
        super(OutletInvoice, self).save(*args, **kwargs)

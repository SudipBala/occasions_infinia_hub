import json
from itertools import repeat
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from satchless.item import ClassifyingPartitioner, ItemList

from delivery.models import OutletOrderDetails, TrackingDetails
from libs.constants import VAT_CHOICES
from libs.fields import CustomJsonField, SizeRestrictedThumbnailerField
from libs.models import HashModel
from libs.utils import get_absolute_media_url
from outlets.outlet_models import Outlet
from outlets.stock_models import OutletStock
from social_app.models import OccasionUser


class OfferBannerModel(models.Model):
    banner_image = SizeRestrictedThumbnailerField("Background Image", upload_to="photos/banners/",
                                                  max_upload_size=10485760, resize_source=dict(size=(300, 0),
                                                                                               sharpen=True,
                                                                                               replace_alpha="#fff"
                                                                                               ),
                                                  max_length=500)
    offer_message = models.TextField("Offer Description", blank=True, help_text="Describe your Store.")
    offer_discount = models.TextField("Offer Discount", blank=True, help_text="Discount percentage")


class OutletItemLine(models.Model):
    """
    certain quantity of a particular stocked_item.
    """
    stocked_item = models.ForeignKey(OutletStock, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(_("Count"), default=1, validators=(
        MinValueValidator(0, "min is zero."),
        MaxValueValidator(1000, "max is thousand."),
    ))

    @property
    def category_slug_name(self):
        return self.stocked_item.category_slug_name

    def get_invoice(self, checkout=False):
        """
        generates invoice of a particular itemline. invoice in a sense that it calculates the necessary costs, applies
        deals and produces final cost.

        :param checkout: bool
        :return: ItemLineInvoice or ItemLineInvoiceDict
        """
        if checkout:
            itemline_invoice = ItemLineInvoice(itemline=self)
        else:
            itemline_invoice = ItemLineInvoiceDict(itemline=self)

        itemline_invoice.actual_price = self.get_total()
        itemline_invoice.net_price = itemline_invoice.actual_price
        itemline_invoice.discount_amount = itemline_invoice.actual_price - itemline_invoice.net_price
        itemline_invoice.save(commit=True)
        return itemline_invoice

    def get_thumbnail(self):
        return get_absolute_media_url(self.stocked_item.get_thumbnail_name())

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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.clean()
        super(OutletItemLine, self).save(force_insert, force_update, using, update_fields)


class OutletCart(HashModel, ItemList):
    """
    DADDY CART contains unique outlet carts(itemlist)
    represents a set of InfiniaLine or other OutletCart objects that has a total price.

    obj : adding itemline to cart using other than id.
        : if same stocked_item appears, sum up their quantities
        : implement get total()
    """

    def __bool__(self):
        return hasattr(self, 'pk')

    def __iter__(self):
        for il in self.itemline.all():
            yield il

    itemline = models.ManyToManyField(OutletItemLine)
    associated_user = models.OneToOneField(OccasionUser, blank=True, null=True, on_delete=models.CASCADE)
    checked_out = models.BooleanField(default=False)

    def add_itemline(self, itemline):
        """

        :param itemline: OutletItemLine
        :return:
        """
        assert isinstance(itemline, OutletItemLine)
        try:
            existing_itemline = self.itemline.get(stocked_item=itemline.stocked_item)
            existing_itemline.quantity += itemline.quantity
            existing_itemline.save()
        except OutletItemLine.DoesNotExist:
            self.itemline.add(itemline)

    def merge_cart(self, cart):
        """
        merges with another cart and returns self

        :param cart: OutletCart
        :return:
        """
        for each_line in cart.itemline.all():
            try:
                self.add_itemline(each_line)
            except ValidationError:
                pass
        return self

    def set_or_update_itemline(self, stock_id, quantity, change):
        try:
            line_item = OutletStock.objects.get(id=stock_id)
        except OutletStock.DoesNotExist:
            raise

        try:
            line = self.itemline.get(stocked_item=line_item)
            if change:
                line.set_quantity(quantity=quantity)
            else:
                line.update_quantity(quantity=quantity)
        except OutletItemLine.DoesNotExist:
            line = OutletItemLine(stocked_item=line_item, quantity=quantity)
            line.save()
            self.itemline.add(line)

    def delete_itemline(self, stock_id):
        line_item = OutletStock.objects.get(id=stock_id)
        name = line_item.get_item_name()
        itemline_instance = self.itemline.get(stocked_item=line_item)
        itemline_instance.delete()
        return name

    def delete_all_itemlines(self):
        self.itemline.all().delete()

    def get_subtotal(self, **kwargs):
        subtotal = 0
        for each_line in self.itemline.all():
            subtotal += each_line.get_total()
        return subtotal

    def __str__(self):
        return "cart %s" % (str(self.id))

    def delete(self, using=None, keep_parents=False, **kwargs):
        # kwargs can contain old residue of deleting a cart with a force_flag
        return super(OutletCart, self).delete(using=None, keep_parents=False)


# @receiver(post_save, sender=OutletCart)
# def check_duplicacy(**kwargs):
#     instance = kwargs["instance"]
#     if hasattr(instance, '_dirty'):
#         return
#     instance._dirty = True
#     all_itemlines = instance.itemline.all()
#     filtered_itemlines = {itemline.stocked_item.id: itemline for itemline in all_itemlines}.values()
#
#     if len(all_itemlines) != len(filtered_itemlines):
#         instance.itemline.remove(*all_itemlines)
#         instance.itemline.add(*filtered_itemlines)
#
#     instance.save()


class CartSplitter(ClassifyingPartitioner):
    """
    Partitions the items in cart into groups based on their stores.
    """

    def classify(self, itemline):
        """
        subject with respect to which cart will be split.

        :type itemline: OutletItemLine
        :return:
        """
        return itemline.stocked_item.outlet.id


class ItemLineDataList(list):
    def __init__(self, *args, **kwargs):
        super(ItemLineDataList, self).__init__(*args, **kwargs)
        self.add = self.append


class ItemLineInvoiceDict(dict):
    def __init__(self, *args, **kwargs):
        super(ItemLineInvoiceDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def save(self, **kwargs):
        pass


class ItemLineInvoice(models.Model):
    itemline = models.ForeignKey('OutletItemLine', on_delete=models.DO_NOTHING)
    actual_price = models.FloatField(_("Actual price"), default=0,
                                     validators=[MinValueValidator(0, "price cant be negative")])
    discount_amount = models.FloatField(_("Discount percentage"), default=0,
                                        validators=[MinValueValidator(0, "discount cant be negative")])
    net_price = models.FloatField(_("Net Price"), default=0,
                                  validators=[MinValueValidator(0, "price cant be negative")])
    unit_selling_price = models.FloatField(_("Unit Selling Price"), null=True)
    unit_marked_price = models.FloatField(_("Unit Marked Price"), null=True)
    quantity = models.FloatField(_("Quantity"), null=True)
    stock_sku = models.CharField(_("SKU"), max_length=40, null=True)
    stock_display_name = models.CharField(max_length=250, null=True)
    date_created = models.DateField(_("Created Date"), default=timezone.now, null=True, blank=True)

    def __str__(self):
        return "%s" % str(self.id)

    def save(self, commit=False, *args, **kwargs):
        if not self.id:
            self.unit_selling_price = self.itemline.stocked_item.price
            self.stock_sku = self.itemline.stocked_item.sku
            self.quantity = self.itemline.quantity
            self.stock_display_name = self.itemline.stocked_item.get_item_name()

        if self.id and not commit:
            raise ValidationError("Can't be saved again.")
        super(ItemLineInvoice, self).save(*args, **kwargs)


class InvoiceDict(dict):
    def __init__(self, *args, **kwargs):
        super(InvoiceDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
        self.itemline_data = ItemLineDataList()
        self.subtotal = 0
        self.additional_discount = 0
        self.shipping_cost = {}
        self.shipping = None
        self.errors = ""

    @property
    def vat(self):
        return VAT_CHOICES.get(self.associated_outlet.country, 0.07)

    def get_shipping_cost(self):
        if isinstance(self.shipping_cost, dict):
            return self.shipping_cost
        cost = json.loads(self.shipping_cost if self.shipping_cost else '{}')
        while True:
            if isinstance(cost, dict):
                return cost
            cost = json.loads(cost)

    @property
    def get_grand_total_without_vat(self):
        return round((self.subtotal - self.additional_discount), 2)

    def get_grand_total(self):
        return (self.subtotal - self.additional_discount) * (1 + self.vat)

    def add_shipping_cost_to_subtotal(self):
        if hasattr(self, '_added'):
            return
        self.subtotal += self.get_shipping_cost().get('price', 0)
        self._added = True

    def save(self, **kwargs):
        self.grand_total = self.get_grand_total()


class OutletInvoice(models.Model):
    invoice_number = models.CharField("Invoice Number", max_length=16)
    associated_cart = models.ForeignKey(OutletCart, null=True, on_delete=models.SET_NULL)
    associated_outlet = models.ForeignKey(Outlet, null=True, on_delete=models.SET_NULL)
    itemline_data = models.ManyToManyField(ItemLineInvoice, blank=True)
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
        return ', '.join([str(il_data.itemline) for il_data in self.itemline_data.all()])

    def _clean_itemline_data(self):
        if not len(set(self.itemline_data.values_list('itemline__stocked_item__outlet', flat=True))) == 1:
            raise ValidationError({"itemline_data": "itemlines dont belong to same outlet."})

    def save(self, commit=False, *args, **kwargs):
        if self.id:
            self._clean_itemline_data()
        self.grand_total = self.get_grand_total_with_shipping_and_vat()
        self.shipping_cost = self.get_shipping_cost()

        if self.id and not commit:
            raise ValidationError("Can't be saved again.")
        super(OutletInvoice, self).save(*args, **kwargs)


class OutletInvoiceDict(dict):
    """
    Collects Invoices of particular outlet together.
    """

    def __init__(self, **kwargs):
        self.invoices = kwargs.pop("invoices")
        if not self.invoices:
            raise ValidationError("Can't initialize without invoices")
        self.subtotal = 0.0
        self.errors = []
        self.user = kwargs.pop("user", None)
        self.checkout = kwargs.pop("checkout", True)
        self.raise_exception = self.checkout
        self.outlet = self.invoices[0].associated_outlet
        super(OutletInvoiceDict, self).__init__()

    def get_subtotal(self, invoices):
        return sum([invoice.subtotal for invoice in invoices])

    @staticmethod
    def append_invoice_errors(invoice, error):
        """

        :param invoice: Invoice # or InvoiceDict
        :param error: list
        :return:
        """
        invoice.is_deliverable = False
        invoice.errors += " ,".join(error)

    def check_errors(self, outlet=None, subtotal=0):
        # error = self.check_outlet_minimum_buy(subtotal=subtotal, outlet=outlet)
        # if False:
        #     self.errors.append(error)
        if self.raise_exception and self.errors:
            raise ValidationError(", ".join(self.errors))
        if not self.raise_exception and self.errors:
            map(OutletInvoiceDict.append_invoice_errors, self.invoices, repeat(self.errors, len(self.invoices)))

    def is_valid(self, *args, **kwargs):
        self.subtotal = self.get_subtotal(self.invoices)
        self.check_errors(outlet=self.outlet, subtotal=self.subtotal)
        for each in self.invoices:
            each.save(commit=True)
        return True


@receiver(pre_delete, sender=OutletInvoice)
def delete_associated_itemlines_invoice(sender, instance, **kwargs):
    instance.itemline_data.all().delete()


class CartInvoice(object):
    """
    Class that will be responsible for the creation of the invoices being checked out(in db) or not(in memory).

    itemline -> sub-cart -> outlet-cart -> cart
    """
    cart = None
    address_id = 0
    user = None
    checkout = False
    daddy_invoice = None

    def __init__(self, **kwargs):
        self.cart = kwargs.pop('cart')
        self.address_id = kwargs.pop('address_id')
        self.shipped_to = kwargs.pop('shipped_to')
        self.user = kwargs.pop('user')
        self.checkout = kwargs.pop('checkout', False)
        self.daddy_invoice = []
        if self.checkout and not self.cart:
            raise ValidationError("Sorry, Cart is empty.")
        if self.checkout and self.cart.associated_user != self.user:
            raise ValidationError("Associated Cart User Does Not Match Authenticated User.")
        super(CartInvoice, self).__init__()

    # for tracking orders
    def track_log(self):
        """
        add the trackers if checked out to the orderDetails logs.
        :return:
        """
        order_details = OutletOrderDetails()
        order_details.save()

        for outlet_invoices in self.daddy_invoice:
            for i in range(len(outlet_invoices)):
                invoice = outlet_invoices[i]

                tracker = TrackingDetails(order=invoice,
                                          buyer=self.user,
                                          shipped_to=self.shipped_to)
                tracker.save()
                order_details.trackers.add(tracker)
                order_details.save()

        return order_details.id

    def get_itemline_invoice(self, itemline):
        """
        One particular itemline in the cart is going to have its own invoice
        :return:
        """
        return itemline.get_invoice(checkout=self.checkout)

    def get_sub_cart_invoice(self, itemlist):
        """
        collects the itemline invoices and packs into a sub-cart invoice


        :type itemlist: ItemList
        :type shipper: int
        :return: Invoice or InvoiceDict
        """
        outlet = itemlist[0].stocked_item.outlet

        if self.checkout:
            invoice_class = OutletInvoice
        else:
            invoice_class = InvoiceDict

        instance = invoice_class(associated_cart=self.cart, associated_outlet=outlet)
        instance.save()

        instance.subtotal = 0
        # todo: after shipping address of user is set
        # if self.address_id and not self.pos_flag:
        #     try:
        #         self.shipped_to = ShippingAddress.objects.get(id=self.address_id)
        #     except ShippingAddress.DoesNotExist:
        #         raise InstantiationException("Missing Shipping Address.")
        #
        #     category_second = itemlist[0].stocked_item.category_slug_name
        #     # cost = self.check_deliverability(outlet, category_second, shipper)
        #     cost = outlet.get_shipping_cost(category_second, self.shipped_to, shipper)
        #
        #     instance.is_deliverable, instance.shipping_cost, instance.shipper = cost[0], cost[1], cost[2]
        #     if not instance.is_deliverable:
        #         category_name = itemlist[0].stocked_item.category_name
        #         error = "{} items from {},{} is not deliverable to your Area. ".format(
        #             ', '.join(category_name).title(),
        #             outlet.display_name.title(),
        #             outlet.area.title()
        #         )
        #         if self.checkout:
        #             # if being checked out, but an item is not deliverable, raise an exception.
        #             instance.delete()
        #             raise InstantiationException(error)
        #         else:
        #             # otherwise simply append it to the invoice.errors
        #             instance.errors += error
        #
        #     instance.shipping = ShippingAddress.objects.get(id=self.address_id)
        #     instance.add_shipping_cost_to_subtotal()

        for each_line in itemlist:
            itemline_invoice = self.get_itemline_invoice(each_line)
            instance.itemline_data.add(itemline_invoice)
            instance.subtotal += itemline_invoice.net_price

        instance.save(commit=True)
        return instance


    @staticmethod
    def append_invoice_errors(invoice, error):
        """

        :param invoice: Invoice # or InvoiceDict
        :param error: str
        :return:
        """
        invoice.is_deliverable = False
        invoice.errors += error
        invoice.save()

    def get_outlet_cart_invoices(self, itemlist):
        """
        collects the independent sub-carts and simply groups them... does no more
        Currently simply checks for outlet's minimum buy stuff

        has its unique shipping address
        :param itemlist: list # of OutletItemLine
        :return:
        """
        outlet = itemlist[0].stocked_item.outlet
        split_data = {1: itemlist}

        subtotal = 0
        invoices = []
        # if outlet is a supermarket, we will split invoices into multiple invoices
        for i in range(len(split_data)):
            invoices.append(
                self.get_sub_cart_invoice(itemlist=list(split_data.values())[i])
            )

        outlet_invoice = OutletInvoiceDict(invoices=invoices,
                                     checkout=self.checkout,
                                     user=self.user)

        outlet_invoice.is_valid()

        return outlet_invoice.invoices

    def get_cart_invoices(self):
        """
        collects the independent outlet-carts and groups them... does no more
        calculates the grand total with vat

        :return: list
        """
        if self.checkout and self.cart.checked_out:
            raise ValidationError({"message": "Cart has already been checked out.", "code": "checked_out"})
        carts = CartSplitter(self.cart.itemline.all())
        grand_total_without_vat = 0
        for outlet_cart in carts:
            with transaction.atomic():
                invoices = self.get_outlet_cart_invoices(outlet_cart)
                grand_total_without_vat += sum([invoice.get_grand_total_without_vat for invoice in invoices])
                self.daddy_invoice.append(invoices)

        if self.address_id and self.checkout:
            self.track_log()
            self.cart.checked_out = True
            self.cart.save()

        return self.daddy_invoice, grand_total_without_vat

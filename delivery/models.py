from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from libs.constants import CURRENCY_CHOICES, STATUS_CHOICES
from libs.models import CustomModel, CustomManager
from libs.utils import get_random_secret_key, prevent_recursion


class TrackingDetailsManager(CustomManager):
    def get_queryset(self):
        return super(TrackingDetailsManager, self).get_queryset().exclude(canceled=True)

    def canceled(self):
        return super(TrackingDetailsManager, self).get_queryset().filter(canceled=True)


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


class TrackingDetails(CustomModel):
    """
    Each invoice is going to have tracking detail with status as in STATUS CHOICES
    """
    tracking_number = models.CharField(_("Tracking Number"), max_length=15, unique=True, help_text=_("Must be unique"),
                                       blank=False)
    status = models.FloatField(_("status"), choices=STATUS_CHOICES, default=0, blank=False)
    _old_status = models.FloatField(_("old status"), choices=STATUS_CHOICES)
    date_modified = models.DateField(_("Altered Date"), help_text=_("when was order altered."))
    date_confirmed = models.DateTimeField(_("Date Confirmed"),
                                          null=True,
                                          help_text=_("when was order confirmed."))
    delivery_date = models.DateTimeField(_("Delivery Date"),
                                         null=True,
                                         help_text=_("when order is to be delivered."))
    order_placed = models.DateTimeField(_("Order Placed"), help_text=_("when was order placed."), default=timezone.now)
    order = models.OneToOneField('outlets.OutletInvoice', on_delete=models.DO_NOTHING)

    shipped_to = models.ForeignKey('social_app.ShippingAddress', on_delete=models.DO_NOTHING, blank=True, null=True)
    buyer = models.ForeignKey('social_app.OccasionUser', null=True, on_delete=models.DO_NOTHING)
    # shipped_to = models.TextField("User Address", null=True, blank=True)
    # buyer = models.("User", null=True, blank=True)

    canceled_date = models.DateTimeField("Canceled Date", null=True)
    canceled = models.NullBooleanField("Canceled", default=False)
    canceled_by = models.OneToOneField("social_app.OccasionUser", null=True, related_name="canceled", on_delete=models.CASCADE)
    # canceled_by = models.TextField("User", null=True, blank=True)
    cancel_reason = models.TextField("Cancel Reason", null=True, blank=False)

    @property
    def get_status(self):
        return STATUS_CHOICES[int(self.status)][1]

    def get_itemlines(self):
        # used in the templates
        itemlines = []
        for il_data in self.order.itemline_data.all():
            itemlines.append({'stocked_item': il_data.itemline.stocked_item,
                              'quantity': il_data.itemline.quantity,
                              'itemline_data': il_data
                              })
        return itemlines

    def reduce_stock(self):
        for itemline_invoice in self.order.itemline_data.all():
            itemline_invoice.itemline.stocked_item.available -= itemline_invoice.itemline.quantity
            itemline_invoice.itemline.stocked_item.save()

    def increment_stock(self):
        for itemline_invoice in self.order.itemline_data.all():
            itemline_invoice.itemline.stocked_item.available += itemline_invoice.itemline.quantity
            itemline_invoice.itemline.stocked_item.save()

    def cancel_order(self, canceled_by, reason):
        if self.canceled and self.canceled_date:
            return False
        self.canceled = True
        self.canceled_date = timezone.now()
        self.canceled_by = canceled_by
        self.cancel_reason = reason
        self.increment_stock()
        self.save()
        return True

    def _change_status(self):
        if self.status == self._old_status:
            return
        if self.status > self._old_status:
            self.date_modified = timezone.now()
            self._old_status = self.status
        elif self.status < self._old_status:
            self.status = self._old_status

    def get_due_date(self):
        # if self.date_confirmed:
        #     return self.date_confirmed + \
        #            datetime.timedelta(hours=float(self.order.get_shipping_cost()['delivery_time']))
        return self.date_confirmed

    def __unicode__(self):
        return self.tracking_number

    # def send_invoice_email(self):
    #     if self.get_status_display().lower() == "pending":
    #         send_invoice_mail(to=[self.order.associated_store.email,
    #                               self.buyer.email,
    #                               settings.CONNECT_EMAIL],
    #                           invoice=self.order)

    # def create_cron_job_delivery_email(self):
    #     # schedule job
    #     task, time = get_delivery_cron_command(self)
    #     os.system("echo %s | at %s" % (task, time))
    #
    # def send_order_confirm_email(self):
    #     if self.get_status_display().lower() == "confirmed" and self._old_status == 0:
    #         self.date_confirmed = timezone.now()
    #         send_order_confirm_mail(to=[self.order.associated_store.email,
    #                                     self.buyer.email],
    #                                 invoice=self.order)
    #         self.delivery_date = self.get_due_date()
    #
    #         self.create_cron_job_delivery_email()
    #
    # def send_order_enroute_email(self):
    #     # send mail with tracking number
    #     pass
    #
    # def send_delivery_email(self):
    #     send_order_due_delivery_mail(to=[self.buyer.email],
    #                                  invoice=self.order)

    def save(self, *args, **kwargs):
        if not self.id:
            self.status = getattr(self, 'status') or 0
            self._old_status = getattr(self, '_old_status') or 0
            self.date_modified = timezone.now()
            self.reduce_stock()
            # send mail
            # self.send_invoice_email()
        else:
            # self.send_order_confirm_email()
            self._change_status()
            # if 'rating' in kwargs.keys():
            #     self.update_ratings(**kwargs.pop('rating'))

        return super(TrackingDetails, self).save(*args, **kwargs)

    objects = TrackingDetailsManager()

    class Meta:
        ordering = ('order_placed', )


class OutletOrderDetails(CustomModel):
    """
    order detail will simply collect an entire, multiple tracking details from a particular user
    """
    order_number = models.CharField(max_length=15, null=False, unique=True)
    trackers = models.ManyToManyField(TrackingDetails)

    @property
    def buyer(self):
        # take first tracker and return its user.
        try:
            return self.trackers.all()[0].buyer
        except IndexError:
            return None

    def get_buyer(self):
        # take first tracker and return its user.
        try:
            return self.trackers.all()[0].buyer
        except IndexError:
            return None

    def send_mail(self):
        pass
        # todo sending to both the client and store

    def __str__(self):
        # except AttributeError:
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            self.order_number = 'O' + get_random_secret_key(10)
        elif self.id and not self.buyer:
            raise AttributeError(_("Empty Cart or Null Buyer..."), code="invalid")
        return super(OutletOrderDetails, self).save(*args, **kwargs)


@receiver(post_save, sender=TrackingDetails)
def add_tracking_num(sender, instance, created=True, **kwargs):
    print("here")
    instance.tracking_number = 'T' + str(instance.id)


# @receiver(post_save, sender=OutletInvoice, dispatch_uid="add_invoice_num")
# def add_invoice_num(sender, instance, **kwargs):
#     instance.invoice_number = 'Inv' + str(instance.id)

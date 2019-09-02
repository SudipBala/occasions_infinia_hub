from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly

from outlets.models import OutletCart
from outlets.stock_models import BaseItem, OutletItem
from .serializers import OutletCartSerializer, ItemLineSerializer
from outlets.models import CartInvoice, OutletCart
from libs.exceptions import CartCheckedOutException, InstantiationException


class OutletCartListView(generics.ListAPIView):
    queryset = OutletCart.objects.all()
    serializer_class = OutletCartSerializer


class OutletCartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OutletCartSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        outletcart=OutletCart.objects.filter(id=self.kwargs['pk'])
        # baseitem= BaseItem.objects.filter(outletitem__outletstock__outletitemline__outletcart__in=outletcart)
        # print(baseitem)
        #outletitemline=OutletItem.objects.filter(outletcart=outletcart)
        return outletcart




# class CartAPIHelperClass(object):
#     SESSION_CART_PARAM = SESSION_ID_PARAM
#
#     def __init__(self, cart_hash, request):
#         self.cart = None
#         self.cart_from_session = False
#         self.request = request
#         if cart_hash:
#             # for token based requests, cart hash is obtained directly
#             if not OutletCart.objects.filter(hash=cart_hash).exists():
#                 raise OutletCart.DoesNotExist
#             self.cart_hash = cart_hash
#         else:
#             self.cart_hash = request.session.get(self.SESSION_CART_PARAM)
#         super(CartAPIHelperClass, self).__init__()
#
#     def get_cart(self):
#         """
#         if not user, session simply has a cart
#
#         if not user.cart or session.cart, return new and set in bot
#
#         if user.cart is same as in session, set user.cart = session.cart
#
#         if user.cart is None but has in session, user.cart = session.cart
#
#         if user.cart exists, but none in session, session.cart = user.cart
#
#         if user.cart exists, session has different cart, user.cart = user.cart + session.cart;
#                                                    then, session.cart = user.cart
#         :return: infiniacart
#         """
#         if self.request:
#             try:
#                 # session_cart aka token_cart; relies on the source of cart_hash
#                 session_cart = OutletCart.objects.get(hash=self.cart_hash)
#             except (MultipleObjectsReturned, ObjectDoesNotExist):
#                 session_cart = None
#             if not self.request.user.is_anonymous():
#                 user = self.request.user
#                 if not hasattr(user, 'outletcart') and session_cart:
#                     self.cart = session_cart
#                     session_cart.associated_user = user
#                     session_cart.save()
#                 elif hasattr(user, 'outletcart') and user.infiniacart == session_cart:
#                     self.cart = session_cart
#                 elif hasattr(user, 'outletcart') and user.infiniacart.__nonzero__() and not session_cart:
#                     self.cart = user.OutletCart
#                 elif bool(hasattr(user, 'outletcart') and session_cart and user.outletcart != session_cart):
#                     # user.cart = user.cart + session.cart;
#                     # then, session.cart = user.cart
#                     user.outletcart.merge_cart(session_cart)
#                     session_cart.delete(force_flag=True)
#                     self.cart = user.outletcart
#                 elif not hasattr(user, 'infiniacart') and not session_cart:
#                     session_cart = OutletCart(associated_user=user)
#                     session_cart.save()
#                     self.cart = session_cart
#             else:
#                 if not session_cart:
#                     session_cart = OutletCart()
#                     session_cart.save()
#                 self.cart = session_cart
#         self.set_cart_in_session()
#         print(self.cart.hash)
#         return self.cart
#
#     def set_cart_in_session(self):
#         self.cart_hash = self.cart.hash
#         if self.request:
#             print("cart hash set in the session.")
#             self.request.session[self.SESSION_CART_PARAM] = self.cart_hash
#             # if not self.request.user.is_anonymous():
#             #     self.request.user.infiniacart = self.cart
#             #     self.request.user.save()
#
#     def remove_cart_from_session(self):
#         self.request.session[self.SESSION_CART_PARAM] = None
#
#     def remove_cart_from_user(self):
#         if self.request:
#             if not self.request.user.is_anonymous:
#                 self.cart.associated_user = None
#                 self.cart.save()
#                 # user = self.request.user
#                 # user.infiniacart = None
#                 # user.save()
#
#     def add_lines_to_cart(self, lines, change, pos=None):
#         cart = self.get_cart()
#         for line in lines:
#             stock_id = line['id']
#             quantity = line['count']
#             mods = line.get('modifier', [])
#             cart.set_or_update_itemline(stock_id=stock_id, quantity=quantity, mods=mods, change=change, pos=pos)
#
#         return cart.itemline.count()
#
#     def read_from_request(self, change, pos=None):
#         """
#         reads items and user from request, and adds itemlines to the cart...
#
#         :return:
#         """
#         items = self.request.data.get("items", [])
#         if not isinstance(items, list):
#             raise ValueError("Expected list of items; got string in items")
#         try:
#             cart_count = self.add_lines_to_cart(items, change, pos=pos)
#             return cart_count
#         except ValueError:
#             raise
#
#     def get_serialized_cart_data(self, address_id=0, shipper_data=None, checkout=False, promo_codes=None, pos_flag=None,
#                                  card_data=None):
#         if not shipper_data:
#             shipper_data = {}
#         # promo_codes = promo_codes or {}
#         cart = self.get_cart()
#
#         if cart is None:
#             raise AttributeError("Cart does not exist.")
#         try:
#             #items to be passed to CartInvoice()
#             # promo_codes = promo_codes,
#             # pos_flag = pos_flag,
#             # card_data = card_data
#             #shipper_data return garako chaina CartInvoice().get_cart_invoices() ley
#             daddy_invoices, grand_total_without_vat, shipper_data = CartInvoice(cart=cart,
#                                                                                 address_id=address_id,
#                                                                                 shipped_to=shipper_data,
#                                                                                 user=self.request.user if not self.request.user.is_anonymous() else None,
#                                                                                 checkout=checkout,
#                                                                                 ).get_cart_invoices()
#             # daddy_invoices, grand_total_without_vat, shipper_data = get_carts_total(
#             #     cart=cart,
#             #     address_id=address_id,
#             #     shipper_data=shipper_data,
#             #     user=request.user if not request.user.is_anonymous() else None,
#             #     checkout=checkout
#             # )
#         except CartCheckedOutException as e:
#             # invalidate the cart in session
#             self.remove_cart_from_session()
#             self.remove_cart_from_user()
#             raise e
#             # checkout page will show all the items and required details of cost, quantity and discount.
#             # return necessary errors
#         # invoices will going to be list of invoices -- invoices contain required info for the checkout page.. that's why
#         # invoicing used rather than using separate function
#         serialized_cart_data = []
#         total = 0
# #upto here --->
#         for invoices in daddy_invoices:
#             for invoice in invoices:
#                 if checkout:
#                     serialized_cart_data.append(InvoiceSerializer(invoice, context={'request': self.request}).data)
#                 else:
#                     serialized_cart_data.append(InvoiceDictSerializer(invoice, context={'request': self.request}).data)
#             total = sum([each["grand_total"] for each in serialized_cart_data])
#         return serialized_cart_data, total, cart.itemline.count(), grand_total_without_vat, shipper_data
#
#     def retrieve_cart_data(self, address_id=0, shipper_data=None, checkout=False, promo_codes=None, pos_flag=None,
#                            card_data=None):
#         shipper_data = shipper_data or {}
#         promo_codes = promo_codes or {}
#         try:
#             serialized_cart_data, total, cart_count, grand_total_without_vat, shipper_data = \
#                 self.get_serialized_cart_data(
#                     address_id=address_id,
#                     shipper_data=shipper_data,
#                     checkout=checkout,
#                     promo_codes=promo_codes,
#                     pos_flag=pos_flag,
#                     card_data=card_data
#                 )
#             if serialized_cart_data:
#                 if checkout:
#                     self.remove_cart_from_session()
#                     self.remove_cart_from_user()
#                 return dict(cart_info=serialized_cart_data,
#                             grand_total_with_vat="{0:.2f}".format(total),
#                             cart_count=cart_count,
#                             grand_total_without_vat=grand_total_without_vat,
#                             shipper_data=shipper_data,
#                             is_deliverable=all([each["is_deliverable"] for each in serialized_cart_data] or [False]),
#                             shipping_address=address_id,
#                             cart_hash=self.cart_hash
#                             )
#             else:
#                 return dict(cart_info=[], cart_hash=self.cart_hash, is_deliverable=False)
#         except (InstantiationException, AttributeError):
#             # return error(e.message)
#             raise


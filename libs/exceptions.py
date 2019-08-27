class CartCheckedOutException(Exception):
    """
    If the cart has already been checked out
    """
class InstantiationException(Exception):
    """
    If the buy doesnot meet the minimum store buying amount
    """
    def get_code(self):
        try:
            return self.message.get('code', 'invalid')
        except AttributeError:
            return None

    def get_message(self):
        try:
            return self.message.get('message', 'invalid')
        except AttributeError:
            return None






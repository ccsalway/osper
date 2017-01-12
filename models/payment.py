import braintree

from environment import *


class Payment(object):
    """Payment processing handler"""

    def __init__(self):
        braintree.Configuration.configure(
            BT_ENVIRONMENT,
            BT_MERCHANT_ID,
            BT_PUBLIC_KEY,
            BT_PRIVATE_KEY
        )

    def public_auth_token(self):
        return braintree.ClientToken.generate()

    def sale_nonce(self, nonce, amount):
        result = braintree.Transaction.sale({
            'amount': amount,
            'payment_method_nonce': nonce,
            'options': {
                "submit_for_settlement": True
            }
        })
        if result.is_success or result.transaction:
            return None
        else:
            # TODO: turn into string array
            return result.message


payment = Payment()
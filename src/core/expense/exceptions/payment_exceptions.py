from ...shared.exception_base import ExceptionBase


class PaymentNotFoundInPurchaseException(ExceptionBase):
    '''Exception raised when a payment is not found in a purchase.'''

    def __init__(self, message: str):
        super().__init__(message)
        self.code = 'PAYMENT_NOT_FOUND_IN_PURCHASE_EXCEPTION'

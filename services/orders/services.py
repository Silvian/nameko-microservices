import random
from time import sleep

from nameko.rpc import rpc, RpcProxy

from .models import Order, OrderStatus


class OrderProcessingService:
    """Order processing service."""

    name = "order_processing_service"
    mail = RpcProxy('email_service')
    sms = RpcProxy('sms_service')

    @rpc
    def process(self, order_details, email, mobile):
        order = self.initiate_order(order_details)
        confirmation = False

        while True:
            rand_val = random.randint(1, 100)
            if order.status == OrderStatus.INITIATED.value:
                if rand_val % 2 == 0:
                    order.status = OrderStatus.PENDING.value

            if order.status == OrderStatus.PENDING.value:
                if rand_val > 80:
                    order.status = OrderStatus.COMPLETE.value

            if order.status == OrderStatus.PENDING.value and not confirmation:
                confirmation = self.send_order_confirmation(email, order)

            if order.status == OrderStatus.COMPLETE.value:
                self.send_dispatch_notification(mobile, order)
                break

            sleep(2)

    @staticmethod
    def initiate_order(details):
        order = Order(details=details)
        sleep(5)
        return order

    def send_order_confirmation(self, email, order):
        subject = "Order confirmation!"
        contents = (
            f"Thank you for placing your order for {order.details}. "
            f"Your order confirmation number is: {order.id}"
        )
        self.mail.send(to=email, subject=subject, contents=contents)
        return True

    def send_dispatch_notification(self, mobile, order):
        message = f"Your order {order.id} has now been dispatched. Order details: {order.details}"
        self.sms.send(mobile=mobile, message=message)
        return True



from typing import Optional

from emroom import Actor


class Barber(Actor):
    queue: "BarberShop"
    customer: Optional["Customer"]

    states = ["IDLE", "CUTTING"]
    haircut_duration = 30

    def __init__(self, queue: "BarberShop"):
        super().__init__(queue.simulation)
        self.queue = queue
        self.customer = None
        self.enqueue(0, self.check_queue)

    def check_queue(self):
        if len(self.queue):
            customer = self.queue.pop()
            self.start_cutting(customer)

    def start_cutting(self, customer: "Customer"):
        self.customer = customer
        self.enter("CUTTING", customer=str(customer))
        self.customer.start_haircut()
        self.enqueue(self.haircut_duration, self.finish_cutting)

    def finish_cutting(self):
        self.enter("IDLE")
        self.customer.end_haircut()
        self.customer = None


from .barber_shop import BarberShop
from .customer import Customer

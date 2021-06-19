from emroom import Simulation, Actor


class BarberShop(Actor):
    customers: list["Customer"]
    barbers: list["Barber"]

    haircut_duration = 30
    states = ["CLOSED", "OPEN"]

    def __init__(self, simulation: Simulation):
        super().__init__(simulation)
        self.customers = []
        self.barbers = []
        self.state = "OPEN"

    def push(self, customer: "Customer"):
        self.customers.append(customer)
        self.log(
            action="push",
            customer=str(customer),
            queue_length=len(self.customers),
        )

    def pop(self) -> "Customer":
        assert self.customers
        customer = self.customers.pop(0)
        self.log(
            action="pop",
            customer=str(customer),
            queue_length=len(self.customers),
        )
        return customer

    def __len__(self):
        return len(self.customers)

    def start_shift(self, barber: "Barber"):
        self.barbers.append(barber)

    @property
    def free_barbers(self):
        return [barber for barber in self.barbers if barber.state == "IDLE"]

    @property
    def waiting_time(self):
        # TODO
        return len(self.customers) * self.haircut_duration


from .customer import Customer
from .barber import Barber

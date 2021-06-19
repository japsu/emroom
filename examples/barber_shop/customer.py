from emroom import Simulation, Actor


class Customer(Actor):
    states = ["IDLE", "WAITING", "BEING_SERVED"]

    waiting_time_threshold = 90
    retry_delay = 24 * 60

    def __init__(self, simulation: Simulation):
        super().__init__(simulation)
        self.enqueue(0, self.get_a_haircut)

    def get_a_haircut(self):
        shortest_queue = sorted(self.simulation.actors(BarberShop), key=lambda queue: queue.waiting_time)[0]

        if shortest_queue.waiting_time <= self.waiting_time_threshold:
            shortest_queue.push(self)
            self.enter("WAITING")
        else:
            self.emit("DISAPPOINTED")
            self.enqueue(self.retry_delay, self.get_a_haircut)

    def start_haircut(self):
        self.enter("BEING_SERVED")

    def end_haircut(self):
        self.enter("IDLE")
        self.emit("HAPPY")


from .barber_shop import BarberShop

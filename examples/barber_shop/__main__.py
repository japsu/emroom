from emroom import Simulation

from .customer import Customer
from .barber_shop import BarberShop
from .barber import Barber


def main(num_queues=1, num_barbers_per_queue=1, num_customers=1):
    simulation = Simulation()

    for i in range(num_customers):
        Customer(simulation)

    for i in range(num_queues):
        queue = BarberShop(simulation)

        for j in range(num_barbers_per_queue):
            Barber(queue)

    simulation.run()


if __name__ == "__main__":
    main()

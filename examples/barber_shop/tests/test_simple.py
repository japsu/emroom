from emroom import Simulation

from ..customer import Customer
from ..barber_shop import BarberShop
from ..barber import Barber


def test_simple_case_finishes():
    simulation = Simulation()
    Customer(simulation)
    queue = BarberShop(simulation)
    Barber(queue)

    simulation.run()

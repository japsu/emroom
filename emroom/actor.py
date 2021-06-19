from collections import Counter
from typing import Callable


class Actor:
    simulation: "Simulation"
    number: int
    signals: Counter
    state: str
    last_state_trans_time: int
    time_spent_in_states: Counter

    states = ["IDLE"]

    def __init__(self, simulation: "Simulation"):
        self.simulation = simulation
        self.number = self.simulation.actor_number_factory(self.__class__)
        self.signals = Counter()
        self.state = "IDLE"
        self.last_state_trans_time = simulation.time
        self.time_spent_in_states = Counter()
        self.simulation.add_actor(self)
        self.log(action="init")

    def __str__(self):
        return f"{self.__class__.__name__}-{self.number}"

    def log(self, **kwargs):
        self.simulation.log(actor=str(self), state=self.state, **kwargs)

    def emit(self, signal, **kwargs):
        self.signals[signal] += 1
        self.log(
            action="emit",
            signal=signal,
            count=self.signals[signal],
            **kwargs,
        )

    def enter(self, new_state, **kwargs):
        assert new_state in self.states

        old_state = self.state
        self.state = new_state

        time_spent = self.time_spent_in_current_state
        self.last_state_trans_time = self.simulation.time
        self.time_spent_in_states[old_state] += time_spent

        self.log(
            action="enter",
            old_state=old_state,
            time_spent=time_spent,
            total_time_spent=self.time_spent_in_states[old_state],
            **kwargs,
        )

    def enqueue(self, time: int, callable: Callable, *args, **kwargs):
        return self.simulation.enqueue(self, time, callable, *args, **kwargs)

    @property
    def time_spent_in_current_state(self):
        return self.simulation.time - self.last_state_trans_time


from .simulation import Simulation

import json
from functools import reduce
from dataclasses import dataclass, field
from queue import Empty, PriorityQueue

from collections import Counter, defaultdict
from typing import Callable, Mapping, Optional, Sequence, Type, TypeVar


T = TypeVar("T")


@dataclass(order=True)
class Event:
    time: int
    actor: "Actor" = field(compare=False)
    callable: Callable = field(compare=False)
    args: Sequence = field(compare=False)
    kwargs: Mapping = field(compare=False)


def sum_counters(counters):
    """
    Combines a bunch of counters.

    >>> c1 = Counter()
    >>> c1["a"] += 5
    >>> c2 = Counter()
    >>> c2["a"] += 1
    >>> c2["b"] -= 6
    >>> sum_counters([c1, c2])
    Counter({'a': 6, 'b': -6})
    """

    result = Counter()
    for counter in counters:
        result.update(counter)
    return result


class Simulation:
    actor_number_sequence: Counter
    time: int
    actors_by_class: defaultdict[Type["Actor"], list["Actor"]]

    # TODO: we don't need synchronization, this may be overkill
    events: PriorityQueue[Event]

    def __init__(self):
        self.actor_number_sequence = Counter()
        self.time = 0
        self.actors_by_class = defaultdict(list)
        self.events = PriorityQueue(maxsize=0)

    def log(self, **kwargs):
        log_obj = dict(time=self.time)
        log_obj.update(kwargs)

        print(json.dumps(log_obj, sort_keys=False))

    def actor_number_factory(self, cls):
        self.actor_number_sequence[cls] += 1
        return self.actor_number_sequence[cls]

    def actors(self, cls: Type[T]) -> list[T]:
        return self.actors_by_class[cls]  # type: ignore

    def add_actor(self, actor: "Actor"):
        self.actors_by_class[actor.__class__].append(actor)

    def enqueue(
        self,
        actor: "Actor",
        time_delta: int,
        callable: Callable,
        *args,
        **kwargs,
    ):
        assert time_delta >= 0, "Time travel is forbidden (tried to enqueue event with a negative time_delta)"

        time = self.time + time_delta
        self.log(actor=str(actor), state=actor.state, action="enqueue", _time=time, _action=callable.__name__)
        self.events.put((Event(time, actor, callable, args, kwargs)))

    def run(self):
        try:
            while event := self.events.get_nowait():
                assert event.time >= self.time, "The structure of time has changed (event occurs in the past)"
                self.time = event.time
                self.log(actor=str(event.actor), state=event.actor.state, action=event.callable.__name__)
                event.callable(*event.args, **event.kwargs)
        except Empty:
            self.log(action="finished", actors=self.dump_actors())

    def dump_actors(self):
        result = {}

        for ActorClass, actors in self.actors_by_class.items():
            result[ActorClass.__name__] = dict(
                signals=sum_counters(actor.signals for actor in actors),
                time_spent_in_states=sum_counters(actor.time_spent_in_states for actor in actors),
            )

        return result


from .actor import Actor

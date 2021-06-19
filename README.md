# Emroom - An actor based simulation environment

In a **simulation** there are **actors** that can ask the simulation to call them back at a specified point in time. These callbacks are called **events** and may have args/kwargs.

When the simulation is run, it will process all such events in a chronological order. An actor may enqueue more events in response to a callback. Once no more events are in the queue, the simulation is **finished**.

## Getting started

### Run the Barber Shop example

No deps (just Python 3.9).

    python -m examples.barber_shop

### Run tests

    pip install pytest
    pytest

## TODO

* [ ] Logging improvements
    * [ ] Log levels or similar filter, eg. `init` and `enqueue` probably need not be shown in most cases
    * [ ] Automatically `str` non-JSON-serializable input
* [ ] Add an option to end the simulation at a specified time (now it runs forever unless it finishes)
* [ ] Perhaps `simulation.run()` should be a generator that yields log events? (Now it just prints them)

## License

MIT
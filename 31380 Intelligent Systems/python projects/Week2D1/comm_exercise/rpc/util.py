import asyncio
from random import random
from itertools import chain, islice


def get_chunks_it(l, n):
    """ Chunks an iterator `l` in size `n`
    Args:
        l (Iterator[Any]): an iterator
        n (int): size of
    Returns:
        Generator[Any]
    """
    iterator = iter(l)
    for first in iterator:
        yield chain([first], islice(iterator, n - 1))


def estimate_pi(n):
    """
        Estimates pi by throwing a point (x,y) randomly *n* times in
        the unit square and counting the number of hits where
        x^2 + Y^2 <= 1.
        Pi is then approximated as 4 * no. hits / n.
        input:
            *n* (int): The number of times to throw the point
        output:
            *estimate* (float): The estimate for pi found here
    """
    hits = sum(int(random()**2 + random()**2 <= 1) for _ in range(n))
    estimate = 4 * hits / n
    return estimate


async def estimate_pi_async(n):
    """
        Estimates pi by throwing a point (x,y) randomly *n* times in
        the unit square and counting the number of hits where
        x^2 + Y^2 <= 1.
        Pi is then approximated as 4 * no. hits / n.
        input:
            *n* (int): The number of times to throw the point
        output:
            *estimate* (float): The estimate for pi found here

        **Note:**
            This is an asynchronous implementation that throws
            100 points before awaiting to relinquish control.
    """
    hits = 0
    for chunk in get_chunks_it(range(n), 100):
        await asyncio.sleep(0)  # Relinquish control so something else can run
        hits += sum(int(random()**2 + random()**2 <= 1) for _ in chunk)
    estimate = 4 * hits / n
    return estimate

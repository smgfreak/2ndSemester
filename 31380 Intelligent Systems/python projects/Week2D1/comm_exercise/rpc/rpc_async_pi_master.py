import asyncio
import sys
from statistics import mean
from math import pi
from time import time
# Import the asynchronous version of ServerProxy
from aioxmlrpc.client import ServerProxy
# Import the asynchronous version of estimate_pi
from util import estimate_pi_async


# Asynchronous call to the slave
async def remote_estimate(n):
    print(f"Requesting that slave estimate pi with {n} throws.")
    # Create the proxy in a nice way so it gets closed when we are done.
    async with ServerProxy('http://localhost:9000') as proxy:
        pi_remote = await proxy.estimate_pi(n)
    print(f"Result of remote estimation: pi={pi_remote:.010f}")
    return pi_remote


# Asynchronous call to ourselves
async def local_estimate(n):
    print(f"Master begins estimating pi with {n} throws.")
    pi_local = await estimate_pi_async(n)
    print(f"Result of local estimation: pi={pi_local:.010f}")
    return pi_local

if __name__ == "__main__":
    # Ensure we got enough arguments coming in
    assert len(sys.argv) >= 2, "Must supply at least 1 argument.\n" + \
        "Usage: rpc_sync_pi_master.py N [argument2 ...]"
    # Split incoming arguments into the number of throws to use.
    # Note that sys.argv[0] is the name of the script itself.
    scriptname, N, *arguments = sys.argv

    # split the workload between ourselves and the remote
    # note: // is integer division
    N = int(N)
    N_remote = N // 2
    N_local = N - N_remote
    start_time = time()

    # ASYNC MAGIC BEGIN
    # Gather up all tasks we have to do, and tell the event loop to
    # run until they are complete.
    futures = asyncio.gather(remote_estimate(N_remote), local_estimate(N_local))
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(futures)
    # ASYNC MAGIC END

    pi_remote, pi_local = results

    pi_m = mean([pi_remote, pi_local])
    print(f"Mean estimation result: pi ={pi_m:.010f}")
    print(f"Relative error: {100*(pi_m/pi - 1):.010f}%")
    print(f"Total time to execute: {time() - start_time} sec")

import sys
from util import estimate_pi
from statistics import mean
from math import pi
from time import time
# Import the synchronous version of ServerProxy
from xmlrpc.client import ServerProxy


# Create the proxy in a nice way so it gets closed when we are done.
with ServerProxy('http://localhost:9000') as proxy:
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

    print(f"Requesting that slave estimate pi with {N_remote} throws.")
    pi_remote = proxy.estimate_pi(N_remote)
    print(f"Result of remote estimation: pi={pi_remote:.010f}")
    print(f"Master begins estimating pi with {N_local} throws.")
    pi_local = estimate_pi(N_local)
    print(f"Result of local estimation: pi={pi_local:.010f}")
    pi_m = mean([pi_remote, pi_local])
    print(f"Mean estimation result: pi ={pi_m:.010f}")
    print(f"Relative error: {100*(pi_m/pi - 1):.010f}%")
    print(f"Total time to execute: {time() - start_time} sec")

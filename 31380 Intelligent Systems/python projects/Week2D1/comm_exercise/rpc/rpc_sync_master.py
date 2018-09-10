from xmlrpc.client import ServerProxy
import sys


# Create the proxy in a nice way so it gets closed when we are done.
with ServerProxy('http://localhost:9000') as proxy:
    # Ensure we got enough arguments coming in
    assert len(sys.argv) >= 3, "Must supply at least 2 arguments.\n" + \
        "Usage: rpc_sync_client.py function argument1 [argument2 ...]"
    # Split incoming arguments into the name of the function to call and
    # the arguments to supply to that function. Note that sys.argv[0] is
    # the name of the script itself.
    scriptname, function, *arguments = sys.argv
    # Get the indicated remote function.
    remote_function = getattr(proxy, function)
    # Print the result of executing the remote function.
    print(remote_function(arguments))

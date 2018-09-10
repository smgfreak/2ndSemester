import logging
from xmlrpc.server import SimpleXMLRPCServer
from util import estimate_pi


def local_estimate_pi(n, *args):
    logging.debug(f'Call received: estimate_pi({n!r})')
    return estimate_pi(n)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)
    # Register the function we are serving
    server.register_function(local_estimate_pi, 'estimate_pi')
    try:
        print("Use Control-C to exit")
        # Start serving our functions
        server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting")

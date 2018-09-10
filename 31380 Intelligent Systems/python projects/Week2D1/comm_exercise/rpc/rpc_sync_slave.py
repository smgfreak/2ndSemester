import logging
import time
from xmlrpc.server import SimpleXMLRPCServer


def reverse_list(l):
    logging.debug(f'Call received: reverse_list({l!r}), calculating for 1 second')
    time.sleep(1)
    return l[::-1]
	
	
def allcaps(l):
	logging.debug(f'ALLCAPS FUNCTION, lower: ({l!r}).')
	lst = []
	for word in l:
		lst.append(word.upper())
	return lst


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)
    # Register the function we are serving
    server.register_function(reverse_list, 'reverse')
    server.register_function(allcaps, 'allcaps')
    try:
        print("Use Control-C to exit")
        # Start serving our functions
        server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting")

import zmq
import sys
import time
from zmq.utils.monitor import recv_monitor_message

port = "5556"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f"tcp://*:{port}")

# Get a monitoring socket where we can sniff information about new subscribers.
monitor = socket.get_monitor_socket()

sub_list = set()

topic = "TIME"
while True:
    # Run through monitoring messages and check if we have new subscribers
    while True:
        try:
            status = recv_monitor_message(monitor, flags=zmq.NOBLOCK)
            print(f"Status: {status}")
            if status['event'] == zmq.EVENT_ACCEPTED:
                print(f"Subscriber \'{status['value']}\' has joined :D")
                sub_list.add(status['value'])
            if status['event'] == zmq.EVENT_DISCONNECTED:
                print(f"Subscriber \'{status['value']}\' has left :(")
                sub_list.remove(status['value'])
        except zmq.Again as e:
            # No more new subscribers - let's stop looking for them
            break
    # Time to publish the latest time!
    messagedata = time.ctime()
    # Note the use of XXX_string here;
    # the non-_string-y methods only work with bytes.
    socket.send_string(f"{topic};{messagedata}")
    print(f"Published topic {topic}: {messagedata} to subscribers: {sub_list}")
    time.sleep(1)

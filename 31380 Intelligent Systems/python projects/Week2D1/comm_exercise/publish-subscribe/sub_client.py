import sys
import zmq

ip = "localhost"
port = "5556"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print(f"Collecting updates from time server at tcp://localhost:{port}")
socket.connect(f"tcp://{ip}:{port}")

# Filter by topic
topicfilter = "TIME"
socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

# Process 5 updates
topic_list = []
for update_nbr in range(5):
    string = socket.recv_string()
    topic, messagedata = string.split(';')
    topic_list.append(messagedata)
    print(f"Received on topic {topic}: {messagedata}")
socket.close()
t_str = "\n".join(topic_list)
print(f"All the times we received: \n{t_str}")

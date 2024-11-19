import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://192.168.50.198:5555")
print("Server listening on port 5555...")

while True:
    message = socket.recv_string()
    print(f"Received message: {message}")
    response = "Thanks for the message!"
    socket.send_string(response)
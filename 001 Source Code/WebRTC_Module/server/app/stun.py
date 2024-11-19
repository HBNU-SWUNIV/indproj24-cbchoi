import socket
import uuid
import struct
import io
import sys


def unpack(stream, fmt):
    size = struct.calcsize(fmt)
    buf = stream.read(size)
    return struct.unpack(fmt, buf)


def stun(host, port=3478):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    transaction_id = uuid.uuid4().bytes
    message_type = b"\x00\x01"  # binding-request
    message_length = b"\x00\x00"
    request = message_type + message_length + transaction_id
    sock.sendto(request, (host, port))
    response, address = sock.recvfrom(2048)
    response_len = len(response)
    response = io.BytesIO(response)

    message_type, message_length = unpack(response, "!HH")
    assert transaction_id == response.read(16)
    assert message_length + 20 == response_len

    response_attributes = []
    while response.tell() < response_len:
        attribute_type, attribute_length = unpack(response, "!HH")
        if attribute_type == 0x0001:  # mapped-address
            zero, family, port = unpack(response, "!BBH")
            assert zero == 0
            assert family == 0x01  # IPv4
            address = socket.inet_ntoa(response.read(4))
            response_attributes.append({
                "address": address,
                "port": port
            })
        else:
            # print("attribute_type", attribute_type)
            response.read(attribute_length)
    return response_attributes

if __name__ == '__main__':
    print(f"내부 IP : {socket.gethostbyname(socket.gethostname())}\n외부 IP : {stun(sys.argv[1], int(sys.argv[2]))}")
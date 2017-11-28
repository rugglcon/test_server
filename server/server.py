"""
The remote server waits for incoming UDP packets and creates a TCP connection
with the client given an IP address and port. The TCP connection can traverse
an intervening NAT router given the initial UDP packet. The address and port
is negotiated via UDP packets.
"""

import json
import socket
import sys

LOCAL_HOST = 'localhost'
LOCAL_PORT = 10001

tcp_data = {}

# create a UDP/IP socket; IPv4, UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind the socket to a port
server_address = (LOCAL_HOST, LOCAL_PORT)
print('Starting server on host: %s, port: %s' % server_address)

try:
    sock.bind(server_address)
    print('Server listening on port: %s' % server_address[1])
except socket.error as e:
    print(sys.stderr, 'Error: %s', e)
    sock.close()
    sys.exit(1)

try:
    while True:

        data, address = sock.recvfrom(1046)
        print('Received %s bytes from %s. data: %s'
              % (len(data), address, data))

        if data:
            try:
                data = json.loads(data)
            except ValueError as e:
                print(sys.stderr, 'Error: %s', e)
                continue
        else:
            continue

        # TODO: do device lookup
        # TODO: should respond logic
        sock.sendto(json.dumps({'should-respond': True}), address)

        if data.get('send-syn', None) is True:
            print('Establishing TCP connection with device on'
                  'host: %s, port: %s' % address)
            tcp_data = data
            break
finally:
    sock.close()

# create a TCP/IP socket; IPv4, TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a port
server_address = (tcp_data['tcp-host'], tcp_data['tcp-port'])

print('Connection to device on host: %s, port: %s' % server_address)
sock.connect(server_address)

try:

    while True:

        # send data
        message = raw_input("Input: ")
        print('Sending message...')
        sock.sendall(message)

        # look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received != amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('Received %s bytes from %s. data: %s'
                  % (len(data), server_address, data))

finally:
    sock.close()

print('TCP session has been terminated.')
sys.exit(0)

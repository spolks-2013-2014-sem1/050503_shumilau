#!/usr/bin/python
import socket
from sys import argv

size = 128;
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
ServerSocket.bind((argv[1],int(argv[2])));
ServerSocket.listen(1);
try:
	while True:
		client, address = ServerSocket.accept();
		while True:
			data = client.recv(size);
			if data:
				client.send(data.lower());
			else:
				break;
finally:
	client.close();

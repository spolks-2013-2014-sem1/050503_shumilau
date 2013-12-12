import socket

buffersize = 1024;

def init(address="", port=1337, isTCP=True):
	if isTCP:
		sockType = socket.SOCK_STREAM;
	else:
		sockType = socket.SOCK_DGRAM;
	ClientSocket = socket.socket(socket.AF_INET, sockType);
	
	return ClientSocket;

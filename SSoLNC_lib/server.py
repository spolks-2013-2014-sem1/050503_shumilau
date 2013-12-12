import socket

buffsize = 1024;

def init(address="", port=1337, isTCP=True):
	if isTCP:
		sockType = socket.SOCK_STREAM;
	else:
		sockType = socket.SOCK_DGRAM;
	try:
		ServerSocket = socket.socket(socket.AF_INET, sockType);
		ServerSocket.bind((address,port));
	except socket.error as msg:
		print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror));
		sys.exit(3);
	if isTCP:
		ServerSocket.listen(5);
		SConnection, address = ServerSocket.accept();
	return SConnection;

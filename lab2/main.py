#!/usr/bin/python
import socket
import sys, getopt

ADDRESS = ""
PORT = 1337
SIZE = 512
helpmsg = "main.py [-a <address>] [-p <port>] [-h]"

try:
   opts, args = getopt.getopt(sys.argv[1:],"ha:p:",["address=","port="]);
except getopt.GetoptError:
   print(helpmsg);
   sys.exit(2);
for opt, arg in opts:
   if opt == '-h':
      print(helpmsg);
      sys.exit(0);
   elif opt in ("-a", "--address"):
      ADDRESS = arg;
   elif opt in ("-p", "--port"):
      PORT = int(arg);

try:
   ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
   ServerSocket.bind((ADDRESS,PORT));
except socket.error as msg:
    print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror))
    sys.exit(3)

ServerSocket.listen(1);
try:
   client, address = ServerSocket.accept();
   while True:
      data = client.recv(SIZE);
      if data:
         client.send(data.lower());
      else:
         break;
finally:
   client.close();

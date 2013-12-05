#!/usr/bin/python
import socket
import sys, getopt

ADDRESS = ""
PORT = 1337
SIZE = 512
helpmsg = "main.py [-a <address>] [-p <port>] [-h]"

try:
   opts, args = getopt.getopt(sys.argv[1:],"h:a:p:",["address=","port="]);
except getopt.GetoptError:
   print(helpmsg);
   sys.exit(2);
for opt, arg in opts:
   if opt == '-h':
      print(helpmsg);
      sys.exit();
   elif opt in ("-a", "--address"):
      ADDRESS = arg;
   elif opt in ("-p", "--port"):
      PORT = int(arg);

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
ServerSocket.bind((ADDRESS,PORT));
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
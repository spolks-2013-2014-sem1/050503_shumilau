#!/usr/bin/python
import socket
import sys
import getopt

ADDRESS = ""
PORT = 1337
SIZE = 512

try:
   opts, args = getopt.getopt(sys.argv[1:],"h:a:p:",["address=","port="]);
except getopt.GetoptError:
   print("main.py -a <address> -p <port>");
   sys.exit(2);
for opt, arg in opts:
   if opt == '-h':
      print("main.py -a <address> -p <port>");
      sys.exit();
   elif opt in ("-a", "--address"):
      ADDRESS = arg;
   elif opt in ("-p", "--port"):
      PORT = int(arg);

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
ServerSocket.bind((ADDRESS,PORT));
ServerSocket.listen(1);
try:
   while True:
      client, address = ServerSocket.accept();
      while True:
         data = client.recv(SIZE);
         if data:
            client.send(data.lower());
         else:
            break;
finally:
   client.close();

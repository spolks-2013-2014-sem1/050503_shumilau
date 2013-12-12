#!/usr/bin/python
import socket
import sys, getopt
import os

sys.path.insert(0,
   os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from SSoLNC_lib import server

address = ""
port = 1337
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
      address = arg;
   elif opt in ("-p", "--port"):
      port = int(arg);

ServerSocket = server.init();

try:
   client, address = ServerSocket.accept();
   while True:
      data = client.recv(1024);
      if data:
         client.send(data.lower());
      else:
         break;
finally:
   client.close();

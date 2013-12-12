#!/usr/bin/python
import socket
import sys, getopt
import os

sys.path.insert(0,
   os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from SSoLNC_lib import server
from SSoLNC_lib import client

ADDRESS = ""
PORT = 1337
FILE = "file"
BUFFSIZE = 64*1024
helpmsg = "main.py [-a <address>] [-p <port>] [-f <path/to/file>] -s|-c|-h"

def srv():
   ServerSocket = server.init();
   SConnection, address = ServerSocket.accept();
   outputFile = open(FILE, "wb");
   while True:
      data = SConnection.recv(BUFFSIZE);
      if not data:
         break;
      outputFile.write(data);
   outputFile.close();
   SConnection.close();

def clt():
   ClientSocket = client.init();
   ClientSocket.connect((ADDRESS, PORT));
   inputFile = open(FILE, "rb");
   while True:
      data = inputFile.read(BUFFSIZE);
      if not data:
         break;
      try:
         if ClientSocket.sendall(data):
            break;
      except:
         print("Failed to send data.");
         break;
   inputFile.close();
   ClientSocket.close();

def main(argv):
   global ADDRESS, PORT, FILE;
   try:
      opts, args = getopt.getopt(argv, "hsca:p:f:", ["address=","port=","file="]);
   except getopt.GetoptError:
      print("Wrong command! Usage:\n", helpmsg);
      sys.exit(2);
   for opt, arg in opts:
      if opt == '-h':
         print(helpmsg);
         sys.exit(0);
      elif opt in ("-a", "--address"):
         ADDRESS = arg;
      elif opt in ("-p", "--port"):
         PORT = int(arg);
      elif opt in ("-f", "--file"):
         FILE = arg;
      elif opt in ("-s", "--server"):
         srv();
      elif opt in ("-c", "--client"):
         clt();

if __name__ == '__main__':
   main(sys.argv[1:])

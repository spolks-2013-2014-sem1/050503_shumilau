#!/usr/bin/python
import socket
import sys, getopt

ADDRESS = ""
PORT = 1337
FILE = "file"
BUFFSIZE = 64*1024
helpmsg = "main.py [-a <address>] [-p <port>] [-f <path/to/file>] -s|-c|-h"

def server():
   try:
      ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
      ServerSocket.bind((ADDRESS, PORT));
      ServerSocket.listen(1);
   except socket.error as msg:
      print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror));
      sys.exit(3);
   SConnection, address = ServerSocket.accept();
   outputFile = open(FILE, "wb");
   while True:
      data = SConnection.recv(BUFFSIZE);
      if not data:
         break;
      outputFile.write(data);
   outputFile.close();
   SConnection.close();

def client():
   ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
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
         server();
      elif opt in ("-c", "--client"):
         client();

if __name__ == '__main__':
   main(sys.argv[1:])

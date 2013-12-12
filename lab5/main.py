#!/usr/bin/python
import socket
import sys, getopt
import os, time
import signal
import fcntl

def sigterm(signo, sigobj):
    print("SIGTERM: {0} Exitting...".format(signo));
    sys.exit(signo);

def server(address="localhost", port=1337, file="tmp", buffsize=1024, isUDP=False):
   try:
      if isUDP:
         ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
         fcntl.fcntl(ServerSocket.fileno(), fcntl.F_SETOWN, os.getpid());
         ServerSocket.bind((address, port));
      else:
         ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
         ServerSocket.bind((address, port));
         ServerSocket.listen(1);
   except socket.error as msg:
      print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror));
      sys.exit(3);
   if not isUDP:
      SConnection, address = ServerSocket.accept();
   outputFile = open(file, "wb");
   while True:
      if isUDP:
         data, address = ServerSocket.recvfrom(buffsize);
      else:
         data = SConnection.recv(buffsize);
      if not data:
         break;
      outputFile.write(data);
   outputFile.close();
   SConnection.close();

def client(address, port, file, buffsize, isUDP):
   if isUDP:
      ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
      fcntl.fcntl(ClientSocket.fileno(), fcntl.F_SETOWN, os.getpid());
   else:
      ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
   if not isUDP:
      ClientSocket.connect((address, port));
   inputFile = open(file, "rb");
   while True:
      data = inputFile.read(buffsize);
      if not data:
         break;
      if not isUDP:
         ClientSocket.send(data);
      else:
         ClientSocket.sendto(data,(address,port));
   inputFile.close();
   ClientSocket.close();

def main(argv):
   address = "";
   port = 1337;
   file = "tmp";
   buffsize = 1024;
   isUDP = False;
   helpmsg = "main.py [-a|--address <address>] [-p|--port <port>] [-f|--file <path/to/file>] [-u|--udp] -s|-c|-h";
   signal.signal(signal.SIGTERM, sigterm);
   signal.signal(signal.SIGINT, sigterm);
   try:
      opts, args = getopt.getopt(argv, "a:p:f:usch", ["address=","port=","file="]);
   except getopt.GetoptError:
      print("Wrong command! Usage:\n", helpmsg);
      sys.exit(2);
   for opt, arg in opts:
      if opt == '-h':
         print(helpmsg);
         sys.exit(0);
      elif opt in ("-a", "--address"):
         address = arg;
      elif opt in ("-p", "--port"):
         port = int(arg);
      elif opt in ("-f", "--file"):
         file = arg;
      elif opt in ("-u", "--udp"):
         isUDP = True;
      elif opt in ("-s", "--server"):
         server(address, port, file, buffsize, isUDP);
         sys.exit(0);
      elif opt in ("-c", "--client"):
         client(address, port, file, buffsize, isUDP);
         sys.exit(0);

if __name__ == '__main__':
   main(sys.argv[1:])

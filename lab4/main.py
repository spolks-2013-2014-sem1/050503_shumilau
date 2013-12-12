#!/usr/bin/python
import socket
import sys, getopt
import os, time
import signal

def sigterm(signo, sigobj):
    print("SIGTERM: {0} Exitting...".format(signo));
    sys.exit(signo);

def sigurg(signo, sigobj):
   try:
      global _conn;
      data = _conn.recv(2, socket.MSG_OOB);
      time.sleep(0.001);
      if data == b"!Q":
         print(recvLen, "/", sendLen);
   except socket.error:
      print("F**k! Error: ", socket.error);

_conn = None;

def server(address, port, file, buffsize):
   try:
      ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
      ServerSocket.bind((address, port));
      ServerSocket.listen(1);
   except socket.error as msg:
      print("Failed to create a socket. Error #{0}: {1}".format(msg.errno, msg.strerror));
      sys.exit(3);
   SConnection, address = ServerSocket.accept();
   global _conn;
   _conn = SConnection;
   signal.signal(signal.SIGURG, sigurg);
   sendLen = int(SConnection.recv(10).decode("utf-8"));
   time.sleep(0.001);
   recvLen = 0;
   outputFile = open(file, "wb");
   while True:
      data = SConnection.recv(buffsize);
      time.sleep(0.001);
      if not data:
         break;
      if data != b"!":
         recvLen += len(data);
         outputFile.write(data);
      else:
         print(recvLen,"bytes recieved of", sendLen, "bytes total.");
   outputFile.close();
   print("Complete!");
   SConnection.close();

def client(address, port, file, buffsize):
   ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
   ClientSocket.connect((address, port));
   ClientSocket.send(bytes(str(os.stat(file).st_size), "utf-8"));
   time.sleep(0.001);
   inputFile = open(file, "rb");
   sentLen = 0;
   sendOob = 1;
   while True:
      data = inputFile.read(buffsize);
      if not data:
         break;
      ClientSocket.send(data);
      time.sleep(0.001);
      sentLen += len(data);
      sendOob -= 1;
      if sendOob == 0:
         sendOob = buffsize;
         if buffsize < 1024*1024:
            sendOob = 1024*1024/buffsize;
         try:
            ClientSocket.send(b"!Q", socket.MSG_OOB);
            print (sentLen, "bytes is sent.");
         except socket.error as e:
            print("Send OOB data error %s" % e);
         time.sleep(0.001);
   inputFile.close();
   ClientSocket.close();

def main(argv):
   address = "";
   port = 1337;
   file = "tmp";
   buffsize = 1024;
   helpmsg = "main.py [-a <address>] [-p <port>] [-f <path/to/file>] -s|-c|-h";
   signal.signal(signal.SIGTERM, sigterm);
   signal.signal(signal.SIGINT, sigterm);
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
         address = arg;
      elif opt in ("-p", "--port"):
         port = int(arg);
      elif opt in ("-f", "--file"):
         file = arg;
      elif opt in ("-s", "--server"):
         server(address, port, file, buffsize);
         sys.exit(0);
      elif opt in ("-c", "--client"):
         client(address, port, file, buffsize);
         sys.exit(0);

if __name__ == '__main__':
   main(sys.argv[1:])

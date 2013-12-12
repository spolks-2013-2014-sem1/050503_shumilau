#!/usr/bin/python

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

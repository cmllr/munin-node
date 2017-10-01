import socket
import sys
import re
from _thread import *
 
HOST = ''
PORT = 4949
VERSION = '0.1.0'
# Thanks to http://www.binarytides.com/python-socket-server-code-example/ for the realy usable example!
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ("failed!" + str(msg.errno))
    sys.exit()

s.listen(10)
 
def output(what):
  return what.encode('utf-8')

def hello():
  hostname = socket.getfqdn();
  return "# munin node at " + hostname + "\n"

def nodes():
  return socket.getfqdn() + "\n.\n";

def version():
  return "munins node on " + socket.getfqdn() + " version: " + VERSION + "\n"

def cap():
  return "cap multigraph dirtyconfig\n"

def plugins():
  return "cpu\n"

def unknown():
  return "# Unknown command. Try cap, list, nodes, config, fetch, version or quit\n"

def clientthread(conn):
    conn.send(output(hello()))  
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        command = data.decode("utf-8")
        regex = re.compile(r"[^\s]+(\s[^\s]+)?")
        extractedCommand = regex.match(command).group()
        if (extractedCommand == "nodes"):
          conn.send(output(nodes()))
        elif (extractedCommand == "help"):
          conn.send(output(unknown()))
        elif (extractedCommand == "version"):
          conn.send(output(version()))
        elif (extractedCommand == "cap"):
          conn.send(output(cap()))
        elif (extractedCommand == "list"):
          conn.send(output(plugins()))
        else:
          conn.send(output(unknown()))
        if not data: 
            break
     
        #conn.sendall(output(reply))
     
    conn.close()
 
while 1:
    conn, addr = s.accept()
    start_new_thread(clientthread ,(conn,))
s.close()
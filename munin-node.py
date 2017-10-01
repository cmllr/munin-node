import socket
import sys
import re
import os
from _thread import *
from subprocess import Popen, PIPE
 
HOST = ''
PORT = 4949
VERSION = '0.1.0'
ENCODING = 'utf-8'
LINEBREAK = '\n'
PLUGINPATH = os.getcwd() + "\\plugins"
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
  return what.encode(ENCODING)

def hello():
  hostname = socket.getfqdn();
  return "# munin node at " + hostname + LINEBREAK

def nodes():
  return socket.getfqdn() + LINEBREAK + "." + LINEBREAK;

def version():
  return "munins node on " + socket.getfqdn() + " version: " + VERSION + LINEBREAK

def cap():
  return "cap multigraph dirtyconfig" + LINEBREAK

def plugins():
  files = [f for f in os.listdir(PLUGINPATH) if os.path.isfile(os.path.join(PLUGINPATH, f))]
  result = ""
  for f in files:
    if (f.endswith(".py")):
      result += f.replace(".py","") + " "
  return result.strip() + LINEBREAK

def unknown():
  return "# Unknown command. Try cap, list, nodes, config, fetch, version or quit" + LINEBREAK

def callMethod(o, name):
    return getattr(o, name)()

def runPlugin(name):
  module = __import__(name.replace("\r",""))
  class_ = getattr(module, name.replace("\r",""))
  instance = class_()
  return callMethod(instance, "fetch")  + LINEBREAK + "." + LINEBREAK

def configPlugin(name):
  module = __import__(name.replace("\r",""))
  class_ = getattr(module, name.replace("\r",""))
  instance = class_()
  return callMethod(instance, "config")  + LINEBREAK + "." + LINEBREAK

def clientthread(conn):
    sys.path.append(PLUGINPATH)
    conn.send(output(hello()))  
    while True:
         
        #Receiving from client
        data = conn.recv(4096)
        command = data.decode(ENCODING)
        regex = re.compile(r"[^\s]+(\s[^\s]+)?")
        extractedCommand = regex.match(command).group()
        print("#"+ extractedCommand + "#")
        if (extractedCommand == "nodes"):
          conn.send(output(nodes()))
        elif (extractedCommand == "help"):
          conn.send(output(unknown()))
        elif (extractedCommand == "version"):
          conn.send(output(version()))
        elif (extractedCommand == "cap"):
          conn.send(output(cap()))
        elif (extractedCommand == "list" or extractedCommand.startswith("list ")):
          conn.send(output(plugins()))
        elif (extractedCommand == "quit"):
          break
        else:
          if (extractedCommand.startswith("fetch ")):
            parts = extractedCommand.split(" ")
            conn.send(output(runPlugin(parts[1])))
          elif (extractedCommand.startswith("config ")):
            parts = extractedCommand.split(" ")
            conn.send(output(configPlugin(parts[1])))
          else:
            conn.send(output(unknown()))
        if not data: 
            sys.exit(5)
     
        #conn.sendall(output(reply))
     
    conn.close()
 
while 1:
    conn, addr = s.accept()
    start_new_thread(clientthread ,(conn,))
s.close()
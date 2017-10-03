import socket
import sys
import re
import os
from _thread import *
from subprocess import Popen, PIPE
import ipaddress

VERSION = ''
ENCODING = 'utf-8'
LINEBREAK = '\n'
PLUGINPATH = os.getcwd() + "\\plugins"
CONFIGS =  {}


class Node:
  def __init__(self):
    self.readConfig()
    self.debug = int(self.getConfigValue("debug",0)) == 1
    if (self.debug):
      print("running in debug mode..")
    self.startServer()
    
  def startServer(self):
    s = None
    try:
      host = self.getConfigValue("host","")
      if (host == "*"):
        host = ""
      port = int(self.getConfigValue("port","4949"))
      if (host == "::1"):
        host = ""
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
      else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      s.settimeout(int(self.getConfigValue("timeout",60)))
      s.bind((host, port))
    except socket.error as msg:
      print ("failed!" + str(msg.errno))
      sys.exit()
    s.listen(10)
    while 1:  
      try:    
        conn, addr = s.accept()
        start_new_thread(self.clientthread ,(conn,))
      except socket.timeout as e:
        pass

  def readConfig(self):
    regex = re.compile(r"^([^\s^#]+)\s{1,}([^\s]+)", re.MULTILINE)
    configFileContent = ""
    with open('munin-node.conf', 'r') as myfile:
      configFileContent=myfile.read()

    for match in regex.finditer(configFileContent):
      config = match.group(1)
      value = match.group(2)
      if (config in CONFIGS):
        oldValue = CONFIGS[config]
        if (isinstance(oldValue, list)):
          CONFIGS[config].append(value)
        else:
          CONFIGS[config] = [oldValue, value]
      else:
        CONFIGS[config] = value

  def getConfigValue(self,value, defaultValue):
    if (value in CONFIGS):
      return CONFIGS[value]
    else:
      return defaultValue

  def output(self,what):
    return what.encode(ENCODING)

  def hello(self):  
    hostname = self.getConfigValue("host_name",socket.getfqdn())
    return "# munin node at " + hostname + LINEBREAK

  def nodes(self):
    return self.getConfigValue("host_name",socket.getfqdn()) + LINEBREAK + "." + LINEBREAK

  def version(self):
    with open(os.getcwd() + '\\.git\\refs\\heads\\master', 'r') as version:
      VERSION=version.read()
    return "munins node on " + self.getConfigValue("host_name",socket.getfqdn()) + " version: " + VERSION + LINEBREAK

  def cap(self):
    return "cap multigraph dirtyconfig" + LINEBREAK

  def plugins(self):
    files = [f for f in os.listdir(PLUGINPATH) if os.path.isfile(os.path.join(PLUGINPATH, f))]
    result = ""
    for f in files:
      if (f.endswith(".py")):
        result += f.replace(".py","") + " "
    return result.strip() + LINEBREAK

  def unknown(self):
    return "# Unknown command. Try cap, list, nodes, config, fetch, version or quit" + LINEBREAK

  def runPlugin(self,name):
    return self.callPluginMethod(name,"fetch")

  def configPlugin(self,name):
    return self.callPluginMethod(name,"config")

  def callPluginMethod(self,name, method):  
    if (name.find(".") == -1 and os.path.isfile(PLUGINPATH + "\\" + name + ".py")): 
      module = __import__(name.replace("\r",""))
      class_ = getattr(module, name.replace("\r",""))
      instance = class_()
      return getattr(instance, method)()  + LINEBREAK + "." + LINEBREAK
    else:
      return "# Unknown service" + LINEBREAK + "." + LINEBREAK
  
  def isPeerAllowed(self, peer):
    allowedPeers = self.getConfigValue("allow",[])
    allowedPeersLength = len(allowedPeers)
    allowedSubnets = self.getConfigValue("cidr_allow",[])
    deniedSubnets = self.getConfigValue("cidr_deny",[])
    matchesAllowedSubnets = self.matchesSubnet(allowedSubnets, peer)
    matchesDeniedSubnets = self.matchesSubnet(deniedSubnets, peer)

    # check if the peer (or a list of peers is)
    if (allowedPeersLength > 0):
      if (isinstance(allowedPeers, list)):
        for i, peerToCheck in enumerate(allowedPeers):
          result = re.match(peerToCheck,peer)
          if (result != None):
            return True
            break
      else:
        result = re.match(allowedPeers,peer)

    if (len(allowedSubnets) > 0):    
      return matchesAllowedSubnets == True and matchesDeniedSubnets == False
    
    if (len(deniedSubnets) > 0):    
      return matchesDeniedSubnets
        
    return False

  def matchesSubnet(self,subnet, peer):
    matches = False
    if (isinstance(subnet, list)):
      if (len(subnet) > 0):
        for i, subnet in enumerate(subnet):
          check = ipaddress.ip_address(peer) in ipaddress.ip_network(subnet)
          if (check):
            matches = True
            break
    else:
      matches = ipaddress.ip_address(peer) in ipaddress.ip_network(subnet)

    return matches

  def clientthread(self, conn):
    sys.path.append(PLUGINPATH)
    if (self.debug):
      print("connection attempt by " + conn.getpeername()[0])
    if (self.isPeerAllowed(conn.getpeername()[0]) == False): 
      if (self.debug):
        print("connection closed for " + conn.getpeername()[0])
      conn.close()
    else:    
      if (self.debug):
        print("connection allowed for " + conn.getpeername()[0])
      conn.send(self.output(self.hello()))  
      while True:        
          #Receiving from client
          data = conn.recv(4096)
          command = data.decode(ENCODING)
          regex = re.compile(r"[^\s]+(\s[^\s]+)?")
          matches = regex.match(command)
          if (matches == None):
            break
            conn.close()
          else:
            extractedCommand = matches.group()
            if (self.debug):
              print("#"+ extractedCommand + "#")
            if (extractedCommand == "nodes"):
              conn.send(self.output(self.nodes()))
            elif (extractedCommand == "help"):
              conn.send(self.output(self.unknown()))
            elif (extractedCommand == "version"):
              conn.send(self.output(self.version()))
            elif (extractedCommand == "cap"):
              conn.send(self.output(self.cap()))
            elif (extractedCommand == "list" or extractedCommand.startswith("list ")):
              conn.send(self.output(self.plugins()))
            elif (extractedCommand == "quit"):            
              conn.close()
              break
            else:
              if (extractedCommand.startswith("fetch ")):
                parts = extractedCommand.split(" ")
                conn.send(self.output(self.runPlugin(parts[1])))
              elif (extractedCommand.startswith("config ")):
                parts = extractedCommand.split(" ")
                conn.send(self.output(self.configPlugin(parts[1])))
              else:
                conn.send(self.output(self.unknown()))   

n = Node()
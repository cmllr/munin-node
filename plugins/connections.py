import subprocess
import re
LINEBREAK = "\n"
class connections:
    def config(self):
        result = "graph_title Connections (TCP and UDP)" + LINEBREAK
        result += "graph_vlabel Network connections" + LINEBREAK
        result += "graph_category network" + LINEBREAK
        result += "tcp.label TCP" + LINEBREAK
        result += "tcp.type GAUGE"  + LINEBREAK
        result += "udp.label UDP" + LINEBREAK
        result += "udp.type GAUGE"
        return result


    def fetch(self):
        result = ""             
        try:
            tcp = subprocess.check_output("netstat -a -n -p tcp", shell=True, stderr=subprocess.STDOUT).decode("ansi")
        except Exception as e:
            tcp = str(e.output)
        result += "tcp.value " + str(len(tcp.split("\r\n"))) + LINEBREAK
        try:
            udp = subprocess.check_output("netstat -a -n -p udp", shell=True, stderr=subprocess.STDOUT).decode("ansi")
        except Exception as e:
            udp = str(e.output)
        result += "udp.value " + str(len(udp.split("\r\n")))
        return result
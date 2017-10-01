import subprocess
import re
LINEBREAK = "\n"
class diskstatus:
    def config(self):
        result = "graph_title Disk Status" + LINEBREAK
        result += "graph_vlabel Disk Status: Reported Problems by WMIC" + LINEBREAK
        result += "graph_category disk" + LINEBREAK
        try:
            output = subprocess.check_output(["wmic", "diskdrive", "get", "status,","caption,","SerialNumber","/format:csv"], shell=True, stderr=subprocess.STDOUT).decode("utf-8")
        except Exception as e:
            output = str(e.output)
        lines = output.split("\r\n")
        for i in range(2,len(lines) -1):           
            infos = lines[i].split(",")
            serial = infos[2].strip()
            disk = infos[1].strip()          
            result += serial + ".label "+ disk + LINEBREAK
            result += serial + ".type GAUGE"  + LINEBREAK
        return result.strip(LINEBREAK)


    def fetch(self):
        result = ""
        try:
            output = subprocess.check_output(["wmic", "diskdrive", "get", "status,","caption,","SerialNumber","/format:csv"], shell=True, stderr=subprocess.STDOUT).decode("utf-8")
        except Exception as e:
            output = str(e.output)
        lines = output.split("\r\n")
        for i in range(2,len(lines) -1):           
            infos = lines[i].split(",")        
            fault = 0
            if (infos[3].strip() != "OK"):
                fault = 1
            result += infos[2].strip() + ".value " + str(fault) + LINEBREAK
        return result.strip(LINEBREAK)
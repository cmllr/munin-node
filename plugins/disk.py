import subprocess
import re
LINEBREAK = "\n"
class disk:
    def config(self):
        result = "graph_title Disks" + LINEBREAK
        result += "graph_vlabel Disk statistics" + LINEBREAK
        result += "graph_category disk" + LINEBREAK
        try:
            output = subprocess.check_output(["wmic", "logicaldisk", "get", "size,","freespace,","caption"], shell=True, stderr=subprocess.STDOUT).decode("utf-8")
        except Exception as e:
            output = str(e.output)
        lines = output.split("\r\n")
        for i in range(1,len(lines)):           
            infos = lines[i]
            matches = re.match("([a-zA-Z]{1})\:[^\d]+(\d+)[^\d]+(\d+)",infos)
            if (matches is not None):
                disk = matches.group(1)
                result += disk + ".label "+ disk + ": used storage " + LINEBREAK
                result += disk + ".total.type GAUGE"  + LINEBREAK
        return result.strip(LINEBREAK)


    def fetch(self):
        try:
            output = subprocess.check_output(["wmic", "logicaldisk", "get", "size,","freespace,","caption"], shell=True, stderr=subprocess.STDOUT).decode("utf-8")
        except Exception as e:
            output = str(e.output)
        lines = output.split("\r\n")
        output =""
        for i in range(1,len(lines)):           
            infos = lines[i]
            matches = re.match("([a-zA-Z]{1})\:[^\d]+(\d+)[^\d]+(\d+)",infos)
            if (matches is not None):
                disk = matches.group(1)
                free = int(matches.group(2)) /1024/1024/1024
                total = int(matches.group(3)) /1024/1024/1024
                percentage = 100 - (100 / ((total/free)))
                output += disk + ".value " + str(round(percentage,2)) + LINEBREAK
        return output.strip(LINEBREAK)
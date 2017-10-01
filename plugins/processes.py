import subprocess
import re
LINEBREAK = "\n"
class processes:
    def config(self):
        result = "graph_title Processes" + LINEBREAK
        result += "graph_vlabel User and System Processes" + LINEBREAK
        result += "graph_category processes" + LINEBREAK
        result += "total.label Total processes" + LINEBREAK
        result += "total.type GAUGE"
        return result

    def fetch(self):
        try:
            output = subprocess.check_output(["wmic", "process", "get", "name"], shell=True, stderr=subprocess.STDOUT).decode("utf-8")
        except Exception as e:
            output = str(e.output)
        lines = output.split("\r\r\n")
        count = 0
        for line in lines:
            if line:
                count+=1
        return "total.value " + str(count -1) # 1 header
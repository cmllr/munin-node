from subprocess import check_output
import re
LINEBREAK = "\n"
class memory:
    def config(self):
        result = "graph_title Memory Usage" + LINEBREAK
        result += "graph_vlabel Load" + LINEBREAK
        result += "graph_category system" + LINEBREAK
        result += "total.label Total installed physical memory" + LINEBREAK
        result += "total.type GAUGE" + LINEBREAK
        result += "used.label Used physical memory" + LINEBREAK
        result += "used.type GAUGE"
        return result

    def getTotalMemory(self):
        got = check_output(["wmic", "computersystem", "get", "TotalPhysicalMemory","/format:value"]).decode("utf-8")
        memory = int(re.search(r'\d+', got).group()) / 1024 /1024 / 1024
        return round(memory,2)

    def getUsedMemory(self):
        got = check_output(["wmic", "os", "get", "FreePhysicalMemory","/format:value"]).decode("utf-8")
        free = int(re.search(r'\d+', got).group()) / 1024 /1024 
        total = self.getTotalMemory()
        used = (total - free)
        return round(used,2)

    def fetch(self):
        got = check_output(["wmic", "computersystem", "get", "TotalPhysicalMemory","/format:value"]).decode("utf-8")
        memory = int(re.search(r'\d+', got).group()) / 1024 /1024 / 1024
        used = self.getUsedMemory()
        return "total.value " + str(round(memory,2)) + LINEBREAK + "used.value " +   str(used)
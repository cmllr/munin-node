from subprocess import check_output
import re
LINEBREAK = "\n"
class cpu:
    def config(self):
        result = "graph_title CPU Usage" + LINEBREAK
        result += "graph_vlabel Load" + LINEBREAK
        result += "graph_category system" + LINEBREAK
        result += "load.label CPU-Load" + LINEBREAK
        result += "load.type GAUGE"
        return result

    def fetch(self):
        got = check_output(["wmic", "cpu", "get", "loadpercentage","/format:value"]).decode("utf-8")
        return "load.value " + str(int(re.search(r'\d+', got).group()))
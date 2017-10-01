import subprocess
import re
from datetime import date, datetime

LINEBREAK = "\n"
class uptime:
    def config(self):
        result = "graph_title Uptime" + LINEBREAK
        result += "graph_vlabel System uptime" + LINEBREAK
        result += "graph_category system" + LINEBREAK
        result += "uptime.label total system uptime" + LINEBREAK
        result += "uptime.type GAUGE"
        return result

    def fetch(self):
        try:
            output = subprocess.check_output(["wmic","os", "get", "lastbootuptime","/format:value"], shell=True, stderr=subprocess.STDOUT).decode("utf-8")
        except Exception as e:
            output = str(e.output)

        regex = re.compile( r"=(\d{4})(\d{2})(\d{2})")
        matches =  regex.search(output)
        boot = date(int(matches.group(1)),int(matches.group(2)),int(matches.group(3)))
        now = datetime.today()
        nowDate = date(now.year, now.month, now.day)
        uptime = nowDate - boot
        return "uptime.value " + str(uptime.days) 
import subprocess
import re
LINEBREAK = "\n"
class users:
    def config(self):
        result = "graph_title Users" + LINEBREAK
        result += "graph_vlabel Logged in users" + LINEBREAK
        result += "graph_category system" + LINEBREAK
        result += "total.label Total users" + LINEBREAK
        result += "total.type GAUGE"
        return result

    def fetch(self):
        try:
            output = subprocess.check_output([r'C:\Windows\Sysnative\query.exe',"user"], shell=True, stderr=subprocess.STDOUT).decode("utf-8")
        except Exception as e:
            output = str(e.output)

        lines = output.split(r"\r\n")

        return "total.value " + str(len(lines) -2 ) # 1 header and 1 last line
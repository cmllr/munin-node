import psutil

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
        return "total.value " + str(len(psutil.users()))
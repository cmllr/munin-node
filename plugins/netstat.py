import psutil

LINEBREAK = "\n"
class netstat:
    def config(self):
        result = "graph_title Netstat" + LINEBREAK
        result += "graph_vlabel overall Traffic (MB)" + LINEBREAK
        result += "graph_category network" + LINEBREAK
        nics = psutil.net_io_counters(True)

        for nic in nics:
            infos = nics[nic]
            name = self.getNICName(nic)
            result += name +"mbytes_sent.label Sent bytes "+nic + LINEBREAK
            result += name +"mbytes_sent.type GAUGE"  + LINEBREAK
            result += name +"mbytes_recv.label Received bytes "+nic + LINEBREAK
            result += name +"mbytes_recv.type GAUGE"  + LINEBREAK
        return result.strip()

        return result

    def getNICName(self, name):
        return name.replace(" ","_")
    def round(self, value):
        return math.ceil(value*100)/100

    def fetch(self):
        result = ""
        nics = psutil.net_io_counters(True)

        for nic in nics:
            infos = nics[nic]            
            name = self.getNICName(nic)
            result += name +"mbytes_sent.value "+ str(round(infos.bytes_sent/8/1024)) + LINEBREAK
            result += name +"mbytes_recv.value "+ str(round(infos.bytes_recv/8/1024)) + LINEBREAK
        return result 
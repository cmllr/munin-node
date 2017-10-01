import subprocess
import re
import psutil
LINEBREAK = "\n"
class diskio:
    def config(self):
        
        result = "graph_title Disk I/O" + LINEBREAK
        result += "graph_vlabel Disk I/O statistics" + LINEBREAK
        result += "graph_category disk" + LINEBREAK
        
        drives = psutil.disk_io_counters(True)

        for drive in drives:
            infos = drives[drive]
            result += drive +"read_bytes.label Read bytes "+drive + LINEBREAK
            result += drive +"read_bytes.type GAUGE"  + LINEBREAK
            result += drive +"write_bytes.label Write bytes "+drive + LINEBREAK
            result += drive +"write_bytes.type GAUGE"  + LINEBREAK
        return result.strip()


    def fetch(self):
        result = psutil.disk_io_counters(True)

        output = ""

        for drive in result:
            infos = result[drive]
            output +=drive + "read_bytes.value "+ str(infos.read_bytes) + LINEBREAK
            output +=drive + "write_bytes.value "+ str(infos.write_bytes) + LINEBREAK
        return output.strip()
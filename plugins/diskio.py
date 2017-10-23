import subprocess
import re
import psutil
import tempfile
import time
import os.path
LINEBREAK = "\n"
class diskio:
    def config(self):
        
        result = "graph_title Disk I/O" + LINEBREAK
        result += "graph_vlabel Bytes read/ wrote" + LINEBREAK
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
        filepath = tempfile.gettempdir() + "diskio.csv"
        lastStats = {}
        if os.path.isfile(filepath):
            with open(filepath) as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.split(";")
                    if len(parts) == 4:
                        lastStats[parts[0]] = [
                            int(parts[1]), # read
                            int(parts[2]), # write
                            int(parts[3]) # unix timestamp
                        ]
        file = open(filepath,"w")         
        output = ""

        for drive in result:
            infos = result[drive]
            read = infos.read_bytes  
            write = infos.write_bytes 
            
            file.write(drive +";"+ str(read) + ";" + str(write) + ";" + str(int(time.time())) + LINEBREAK)
            if drive in lastStats:
                read -= lastStats[drive][0]         
                write -= lastStats[drive][1]   

            output +=drive + "read_bytes.value "+ str(read) + LINEBREAK
            output +=drive + "write_bytes.value "+ str(write) + LINEBREAK

        file.close()
        return output.strip()
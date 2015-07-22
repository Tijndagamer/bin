#!/usr/bin/python

import os
import time
import re

def main():
    dataList = []

    dataList.append(os.popen("uptime").read() + "\n")
    dataList.append(os.popen("cpuload").read())
    dataList.append("CPU temp: \n" + os.popen("getcputemp").read())
    dataList.append("Network stats:\n" + os.popen("getdown").read())
    dataList.append(os.popen("getup").read() + "\n")
    dataList.append("Memory stats:\n" + os.popen("free -h").read() + "\n")
    dataList.append("Drive stats:  TOTAL | USED | FREE\n" + os.popen("df -h | grep '/dev/' && df -h --total | grep 'total'").read())

    data = str(dataList)
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data.replace(',', '')

    #os.popen("echo " + data + " > /var/www/html/status")
    #for data in dataList:
    #    print data
    
    with open("/var/www/html/status.txt", "w") as file:
        for data in dataList:
            file.write(data)
            
    with open("/var/www/html/temp.txt", "a+") as file:
        file.write(re.search("(\d\d\:\d\d\:\d\d)", os.popen("uptime").read(), re.VERBOSE).group(0) + "/n")
        file.write(re.search("CPU\:\s([\d\.]+)\SC", os.popen("getcputemp").read(), re.VERBOSE).group(1) + "C\n")
        
    with open("/var/www/html/load.txt", "a+") as file:
        file.write(re.search("(\d\d\:\d\d\:\d\d)", os.popen("uptime").read(), re.VERBOSE).group(0) + "/n")
        file.write(re.search("CPU\sload\:\s([\d\.]+\%)", os.popen("cpuload").read(), re.VERBOSE).group(1) + "\n")
    
while True:
    main()
    time.sleep(300)

from PASSWORD import username, password
import re
import paramiko
import openpyxl
import os
import multiprocessing
from termcolor import colored
import datetime
import pandas as pd
import threading
from queue import Queue
import pandas as pd
import time, smtplib

def policy():
    ExcelExport = [["Cisco", "INT", "Tanımlama"]]

														  

    my_connection = paramiko.SSHClient()
    my_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    IP_Core = "172.16.189.23" # Connecting device via SSH

    try:
        my_connection.connect(IP_Core, port="22", username=username, password= password, timeout=15)
        remote_connection = my_connection.invoke_shell()

        print(colored("Establised_NEXUS:" + IP_Core, "yellow"))

        remote_connection.send(" terminal length 0" + "\n")
        time.sleep(1)
        remote_connection.send("show running-config " + " \r")
        time.sleep(1)
        cikti = remote_connection.recv(65000)
        sonuc20 = cikti.decode('ascii').strip("\n")

        My_file = "syslog_spines.txt" # To see abnormal characters in "sonuc20"
        syslog = open(My_file, 'w')
        syslog.write(sonuc20)
        syslog.close()
# #############################################################
        with open("syslog_spines.txt", "r") as f: 
            my_each_data11 = f.readlines()
            my_each_data12 = "".join(my_each_data11)
            my_each_data15= my_each_data12.strip("")
            my_each_data = my_each_data15.split()
            #print(my_each_data)

        my_each_data25 = []

        for line in my_each_data:
            my_each_data5 = line.strip('\n')
            my_each_data25.append(my_each_data5)

        idxes = []

        for i in range(len(my_each_data25)):
            if my_each_data25[i] == "!": # All "my_each_data" which "(!)" located
                idxes.append(i)

        # print(idxes[0]+1)
        my_each_data26 = []
        my_each_data4 = []

        e = 0
        d = 0
        while True: # Every data between "!" mares
            v = 1
            while idxes[d] + v < idxes[e + 1]: 
                my_each_data4.append(my_each_data25[idxes[d] + v])
                v = v + 1

                if idxes[d] + v == idxes[e + 1]: 
                    my_each_data26.append(my_each_data4) 
                    my_each_data4 = []
            d = d + 1
            e = e + 1

            if e + 1 == len(idxes):
                break
# ####################################################

        for BE in my_each_data26:
            BE1 = " ".join(BE)
            if "Bundle-Ether" in BE1:
                BE91 = BE1.split()
                BE96 = BE91[1]
                BE99 = BE96.split(".")

                if len(BE99) > 1 and int(BE99[1]) > 150 and "transport" not in BE91 and "service-policy" not in BE91:
                    BE91.remove("description")
                    BE90 = BE99[0] +"."+ BE99[1]
                    print(BE90)
                    ExcelExport.append([IP_Core, BE90, BE91[2]])


    except Exception as e:
        print("no connectivity" + IP_Core +"\n")
        time.sleep(2)
        with open("ulasilamayan ipler.txt", "a") as f:
            f.write(IP_Core + "\n")
        f.close()


policy()

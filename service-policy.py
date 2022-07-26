def policy():
    ExcelExport = [["Cisco", "INT", "Tanımlama"]]

														  

    my_connection = paramiko.SSHClient()
    my_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    IP_Core = "172.16.189.23" # Connecting device via SSH

    try:
        my_connection.connect(IP_Core, port="22", username=username, password= password, timeout=15)
        remote_connection = my_connection.invoke_shell()

        print(colored("Connected_ASR:" + IP_Core, "yellow"))

        remote_connection.send(" terminal length 0" + "\r")
        time.sleep(1)
        remote_connection.send("show running-config interface" + " \r")
        time.sleep(1)
        out12 = remote_connection.recv(9999)
        res12 = out12.decode('ascii').strip("\n")

        My_file = "syslog_dc1.txt" # To see unexpected characters in "res12"
        syslog = open(My_file, 'w')
        syslog.write(res12)
        syslog.close()
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        with open("syslog_dc1.txt", "r") as f: 
            my_each_data11 = f.readmy_each_data()
            my_each_data12 = "".join(my_each_data11)
            my_each_data15= my_each_data12.strip("")
            my_each_data = my_each_data15.split()
            #print(my_each_data)

        my_each_data2 = []

        for line in my_each_data:
            my_each_data5 = line.strip('\n')
            my_each_data2.append(my_each_data5)

        indices = []

        for i in range(len(my_each_data2)):
            if my_each_data2[i] == "!": # All "my_each_data" which "(!)" located
                indices.append(i)

        # print(indices[0]+1)
        my_each_data3 = []
        my_each_data4 = []

        k = 0
        j = 0
        while True: # Every data between "!" marks
            v = 1
            while indices[j] + v < indices[k + 1]: 
                my_each_data4.append(my_each_data2[indices[j] + v])
                v = v + 1

                if indices[j] + v == indices[k + 1]: 
                    my_each_data3.append(my_each_data4) 
                    my_each_data4 = []
            j = j + 1
            k = k + 1

            if k + 1 == len(indices):
                break
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        for BE in my_each_data3:
            BE1 = " ".join(BE)
            if "Bundle-Ether" in BE1:
                BE2 = BE1.split()
                BE3 = BE2[1]
                BE4 = BE3.split(".")

                if len(BE4) > 1 and int(BE4[1]) > 200 and "transport" not in BE2 and "service-policy" not in BE2:
                    BE2.remove("description")
                    BE5 = BE4[0] +"."+ BE4[1]
                    print(BE5)
                    ExcelExport.append([IP_Core, BE5, BE2[2]])


    except Exception as e:
        print("no connectivity" + IP_Core +"\n")
        time.sleep(2)
        with open("unreachables_CISCO.txt", "a") as f:
            f.write(IP_Core + "\n")
        f.close()


policy()

def policy():

    ExcelExport = [["Device", "Interface", "Description"]]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    DC_IP = "10.214.68.16" # A device that is connected via SSH

    try:
        ssh.connect(DC_IP, port="2222", username=username, password= password, timeout=20)
        remote_connection = ssh.invoke_shell()

        print(colored("Connected_ASR:" + DC_IP, "blue"))

        remote_connection.send(" terminal length 0" + "\r")
        time.sleep(2)
        remote_connection.send("show running-config interface" + " \r")
        time.sleep(2)
        output3 = remote_connection.recv(99999999)
        result3 = output3.decode('ascii').strip("\n")

        LOGfile = "log_dc1.txt" # as we received unexpected characters in "result3", its been added into a log file. 
        log = open(LOGfile, 'w')
        log.write(result3)
        log.close()
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        with open("log_dc1.txt", "r") as f: 
            lines6 = f.readlines()
            lines5 = "".join(lines6)
            lines7= lines5.strip("")
            lines = lines7.split()
            #print(lines)

        lines2 = []

        for line in lines:
            lines5 = line.strip('\n')
            lines2.append(lines5)

        indices = []

        for i in range(len(lines2)):
            if lines2[i] == "!": # All lines where "exclamation marks(!)" are located
                indices.append(i)

        # print(indices[0]+1)
        lines3 = []
        lines4 = []

        k = 0
        j = 0
        while True: # Each data between sequent exclamation marks
            v = 1
            while indices[j] + v < indices[k + 1]: 
                lines4.append(lines2[indices[j] + v])
                v = v + 1

                if indices[j] + v == indices[k + 1]: 
                    lines3.append(lines4) 
                    lines4 = []
            j = j + 1
            k = k + 1

            if k + 1 == len(indices):
                break
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        for x in lines3:
            x1 = " ".join(x)
            if "Bundle-Ether" in x1:
                x2 = x1.split()
                x3 = x2[1]
                x4 = x3.split(".")

                if len(x4) > 1 and int(x4[1]) > 200 and "l2transport" not in x2 and "service-policy" not in x2 and "description" in x2 and "shutdown" not in x2:
                    x2.remove("description")
                    x5 = x4[0] +"."+ x4[1]
                    print(x5)
                    ExcelExport.append([DC_IP, x5, x2[2]])


    except Exception as e:
        print("no connectivity_" + DC_IP +"\n")
        time.sleep(2)
        with open("unreachables_CISCO.txt", "a") as f:
            f.write(DC_IP + "\n")
        f.close()


policy()

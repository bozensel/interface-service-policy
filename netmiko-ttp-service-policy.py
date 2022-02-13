def policy():
        ExcelExport = [["Description", "Interface", "Input_Policy","Output_Policy"]]
        ciscoasr9k = { "host" : "1.1.1.1","username" :"admin","password" :"admin","port" : 22,"device_type" : "cisco_xr",}
        conn = ConnectHandler(**ciscoasr9k)
        conn.enable()
        data_to_parse = conn.send_command_timing('show run interface')

        ttp_template = """
interface Bundle-Ether{{ interface_Bundle | split(".") }}
 description {{ Description }}
 service-policy input {{ qos_input }}
 service-policy output {{ qos_output}}
"""
        # create parser object and parse data using template:
        parser = ttp(data=data_to_parse, template=ttp_template)
        parser.parse()

        # print result in JSON format

        results = parser.result(format='json')[0]
        result = json.loads(results)

        #print(result[0])

        #for i in result[0]:
                #print(int(i["interface_Bundle"][0]))


        for i in result[0]:
                if len(i["interface_Bundle"]) > 1 and int(i["interface_Bundle"][1]) > 200 and "Description" in i and i["interface_Bundle"][1] != "311" and i["interface_Bundle"][1] !=  "202"  and i["interface_Bundle"][1] !=  "203"  and i["interface_Bundle"][1] !=  "204"  and i["interface_Bundle"][1] !=  "205"  and i["interface_Bundle"][1] !=  "220"  and i["interface_Bundle"][1] !=  "227"  and i["interface_Bundle"][1] !=  "262"  and i["interface_Bundle"][1] !=  "276"  and i["interface_Bundle"][1] !=  "280"  and i["interface_Bundle"][1] !=  "300"  and i["interface_Bundle"][1] !=  "308"  and i["interface_Bundle"][1] !=  "309"  and i["interface_Bundle"][1] !=  "310"  and i["interface_Bundle"][1] !=  "322"  and i["interface_Bundle"][1] !=  "324"  and i["interface_Bundle"][1] !=  "340"  and i["interface_Bundle"][1] !=  "341"  and i["interface_Bundle"][1] !=  "347"  and i["interface_Bundle"][1] !=  "350"  and i["interface_Bundle"][1] !=  "356"  and i["interface_Bundle"][1] !=  "405"  and i["interface_Bundle"][1] !=  "1225"  and i["interface_Bundle"][1] !=  "1474"  and i["interface_Bundle"][1] !=  "1632"  and i["interface_Bundle"][1] !=  "320"  and i["interface_Bundle"][1] !=  "747" :
                        if "qos_input" not in i:
                                interface_Bundle2 = "interface_Bundle"+str(i["interface_Bundle"][0]) +"."+ str(i["interface_Bundle"][1])
                                #ExcelExport.append([i["Description"],interface_Bundle2,i["qos_input"],i["qos_output"]])
                                ExcelExport.append([i["Description"],interface_Bundle2,"none", "none"])



        XLSExport(ExcelExport, "Policy", "policy1.xlsx")
        SendMailwAttachment_(ExcelExport, "policy1.xlsx")

while True:
    schedule.run_pending()
    time.sleep(1)

policy()

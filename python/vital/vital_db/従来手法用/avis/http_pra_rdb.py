import requests
import json
import iris
import time
import datetime


url = "http://localhost:2528/api/info"


res = requests.get(url)
dt_now = datetime.datetime.now()
#print(res.text)
info_t = res.text    #文字列として取得
info = json.loads(info_t)

args = {"hostname" : "192.168.11.3", "port" : 1972,
"namespace" : "FS", "username" : "_SYSTEM", "password" : "bmi-2718"
}


connection = iris.connect(**args)
irispy = iris.createIRIS(connection)
if info["VitalInfo"][0]["model"] == "WS-M50BT":

    vital = []
    # macaddr = info["VitalInfo"][0]["macAddr"]
    # low_bp = info["VitalInfo"][2]["diastole"]
    # mean_bp = info["VitalInfo"][2]["mean"]
    # high_bp = info["VitalInfo"][2]["systole"]
    # pulse = info["VitalInfo"][3]["pulse"]
    vital.append(info["VitalInfo"][0]["macAddr"])
    vital.append([info["VitalInfo"][2]["diastole"],"diastole", json.dumps({"unit" : "mmHg", "format" : "inaoka_vital"})] )
    vital.append([info["VitalInfo"][2]["mean"], "mean", json.dumps({"unit" : "mmHg", "format" : "inaoka_vital"})])
    vital.append([info["VitalInfo"][2]["systole"], "systole", json.dumps({"unit" : "mmHg", "format" : "inaoka_vital"})])
    vital.append([info["VitalInfo"][3]["pulse"], "pulse",json.dumps({"unit" : "拍/分", "format" : "inaoka_vital"}, ensure_ascii=False)])
    MID = irispy.classMethodValue("vital.measure", "getmaxID")
    if MID == None:
        num = 1
        for i in range(1,len(vital)):
            MID += "measure_" + str(num)
            d = {"entity": vital[0], "role": vital[i][1], "databody": vital[i][0], "Temporal": dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'), "property" : vital[i][2]}
            print(d)
            insert_vital = irispy.classMethodValue("vital.measure", "Insert", MID, vital[0], vital[i][1],vital[i][0], dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'))
            num += 1
    else:
        for i in range(1,len(vital)):
            MId = "measure_" + str(int(MID)+1)
            d = {"entity": vital[0], "role": vital[i][1], "databody": vital[i][0], "Temporal": dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'), "property" : vital[i][2]}
            print(d)
            insert_vital = irispy.classMethodValue("vital.measure", "Insert", str(MID), vital[0], vital[i][1],vital[i][0], dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'))

elif info["VitalInfo"][0]["model"] == "BO-750":
    macaddr = info["VitalInfo"][0]["macAddr"]
    sa = info["VitalInfo"][1]["saturation"]
    MID = irispy.classMethodValue("vital.measure", "getmaxID")
    if MID == None:
        MID = "measure_1"
        d = {"entity": macaddr, "role": "saturation", "databody": sa, "Temporal": dt_now.strftime('%Y/%m/%d %H:%M:%S.%f')}
        print(d)
        insert_vital = irispy.classMethodValue("vital.measure", "Insert", MID, macaddr, "saturation", sa, dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'))

    else:
        MID = "measure_" + str(int(MID)+1)
        d = {"entity": macaddr, "role": "saturation", "databody": sa, "Temporal": dt_now.strftime('%Y/%m/%d %H:%M:%S.%f')}
        print(d)
        insert_vital = irispy.classMethodValue("vital.measure", "Insert", MID, macaddr, "saturation", sa, dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'))



elif info["VitalInfo"][0]["model"] == "MT-500":
    macaddr = info["VitalInfo"][0]["macAddr"]
    bt = round(info["VitalInfo"][1]["body"], 1)
    MID = irispy.classMethodValue("vital.measure", "getmaxID")
    if MID == None:
        MID = "measure_1"
        d = {"entity": macaddr, "role": "bodytempurture", "databody": bt, "Temporal": dt_now.strftime('%Y/%m/%d %H:%M:%S.%f')}
        print(d)
        insert_vital = irispy.classMethodValue("vital.measure", "Insert", MID, macaddr, "bodytempurture", bt, dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'))

    else:
        MID = "measure_" + str(int(MID)+1)
        d = {"entity": macaddr, "role": "bodytempurture", "databody": bt, "Temporal": dt_now.strftime('%Y/%m/%d %H:%M:%S.%f')}
        print(d)
        insert_vital = irispy.classMethodValue("vital.measure", "Insert", MID, macaddr, "bodytempurture", bt, dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'))

else:
    print("error")

connection.close()
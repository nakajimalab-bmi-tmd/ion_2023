import requests
import json
import irisnative
import time
import datetime


url = "http://localhost:2528/api/info"


res = requests.get(url)
dt_now = datetime.datetime.now()
#print(res.text)
info_t = res.text    #文字列として取得
info = json.loads(info_t)

ip = "192.168.11.3"
port = 1972
namespace = "FS"
username = "_SYSTEM"
password = "bmi-2718"

connection = irisnative.createConnection(ip, port,namespace,username,password)
iris_native = irisnative.createIris(connection)
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
    for i in range(1,len(vital)):
        d = {"entity": vital[0], "role": vital[i][1], "databody": vital[i][0], "Temporal": dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'), "property" : vital[i][2]}
        print(d)
        insert_vital = iris_native.classMethodValue("ion.bital", "Insert", vital[i][1], vital[0], None, vital[i][0], dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'), None, vital[i][2])

elif info["VitalInfo"][0]["model"] == "BO-750":
    macaddr = info["VitalInfo"][0]["macAddr"]
    sa = info["VitalInfo"][1]["saturation"]
    d = {"entity": macaddr, "role": "saturation", "databody": sa, "Temporal": dt_now.strftime('%Y/%m/%d %H:%M:%S.%f')}
    print(d)
    insert_vital = iris_native.classMethodValue("ion.bital", "Insert", "saturation", macaddr, None, sa, dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'), None, json.dumps({"unit" : "%", "format" : "inaoka_vital"}))


elif info["VitalInfo"][0]["model"] == "MT-500":
    macaddr = info["VitalInfo"][0]["macAddr"]
    bt = round(info["VitalInfo"][1]["body"], 1)
    d = {"entity": macaddr, "role": "bodytempurture", "databody": bt, "Temporal": dt_now.strftime('%Y/%m/%d %H:%M:%S.%f')}
    print(d)
    insert_vital = iris_native.classMethodValue("ion.bital", "Insert", "bodytempurture", macaddr, None, bt, dt_now.strftime('%Y/%m/%d %H:%M:%S.%f'), None, json.dumps({"unit" : "℃", "format" : "inaoka_vital"}, ensure_ascii=False))

else:
    print("error")

connection.close()
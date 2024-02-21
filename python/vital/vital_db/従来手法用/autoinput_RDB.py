import iris
import datetime
import pprint

# Open a connection to the server
args = {'hostname':'192.168.0.67', 'port':1972,
    'namespace':'FS', 'username':'_SYSTEM', 'password':'bmi-2718'
}
conn = iris.connect(**args)
# Create an iris object
irispy = iris.createIRIS(conn)


def query(E, R, T):
    q = {"患者番号" : E, "バイタル名" : R, "時間" : T}

    return q

#登録デバイスの取得
def get_IRISobj_ls_DE(cls, DType, start, end):  
    ls_obj_DE = []
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            if (DType == obj.get("deviceType")):
                ls_obj_DE.append([obj.get("deviceID"), obj.get("deviceType")])

    return ls_obj_DE

#ある患者の使用履歴
def get_IRISobj_ls_his(cls, PID, DID, start, end):  
    ls_obj_his = []
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            if (PID == obj.get("PID")) and (DID == obj.get("deviceID")):
                ls_obj_his.append([obj.get("PID"), obj.get("deviceID"), obj.get("useTime")])

    return ls_obj_his

#バイタル取得
def get_IRISobj_ls_mes(cls, DID, VN, T, start, end):  
    ls_obj_his = []
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            if (VN == obj.get("vitalname")) and (DID == obj.get("deviceID")) and (T == obj.get("Time")):
                ls_obj_his.append([obj.get("PID"), obj.get("vitalname"), obj.get("Time"), obj.get("value")])

    return ls_obj_his

def get_IRISobj_ls_result(cls, PID, num):
    
    obj = irispy.classMethodObject(cls, "%OpenId", str(num))

    return [PID, obj.get("vitalname"), obj.get("Time"), obj.get("value")]

def check_irre_pa(maxID,useDN):
    time = datetime.datetime.strptime(useDN[2],'%Y/%m/%d %H:%M:%S.%f')
    time_duration = time + datetime.timedelta(minutes=20)
    period = 1200
    for i in range(1, maxID+1):
        if irispy.classMethodValue("vital.history", "existobject", i) == 1:
            if  useDN[0] != irispy.classMethodObject("vital.history", "%OpenId", str(i)).get("deviceID") and irispy.classMethodObject("vital.history", "%OpenId",str(i)).get("deviceID") == useDN[1] and (time < datetime.datetime.strptime(irispy.classMethodObject("vital.history", "%OpenId", str(i)).get("useTime"), '%Y/%m/%d %H:%M:%S.%f') < time_duration):
                diff = datetime.datetime.strptime(irispy.classMethodObject("vital.hisotry","%OpenId", str(i)).get("useTime"), '%Y/%m/%d %H:%M:%S.%f') - time
                period = diff.total_seconds()
            else:
                continue
    
    return period
                                                
                                    



if __name__ == '__main__':



    #クエリ作成
    q = query("PID001", "体温", "2023/08/02")

    #IRIS内の最大IDを取得
    maxID_his = int(irispy.classMethodValue("vital.history", "getmaxID"))
    maxID_mea = int(irispy.classMethodValue("vital.measure", "getmaxID"))
    #患者間での測定の最低時間
    period = 1200

    #自動入力の流れ
    if q["バイタル名"] == "体温":
            #パルスの機器ID取得　ls_deは二重配列
            ls_de = get_IRISobj_ls_DE("vital.DeviceEntry", "体温計", 1, 4)
            
            #print(ls_de)
            #使用履歴の獲得　ls_de_useは二重配列
            ls_de_use = []
            for i in range(len(ls_de)):
                ls = get_IRISobj_ls_his("vital.history", q["患者番号"], ls_de[i][0], 1, maxID_his+1)
                for i in range(len(ls)):
                    ls_de_use.append(ls[i])

            #print(ls_de_use)
            #イレギュラーチェック
            for i in range(len(ls_de_use)):
                period = check_irre_pa(maxID_his, ls_de_use[i])     
                ls_de_use[i].append(period)   

            #print(ls_de_use)

            result_ls = []
            for i in range(len(ls_de_use)):
                for j in range(1, maxID_mea+1):
                    if irispy.classMethodValue("vital.measure", "existobject", j) == 1:
                        if ls_de_use[i][1] == irispy.classMethodObject("vital.measure", "%OpenId", str(j)).get("deviceID") and (0 <= (datetime.datetime.strptime(irispy.classMethodObject("vital.measure", "%OpenId", str(j)).get("Time"),'%Y/%m/%d %H:%M:%S.%f')  - datetime.datetime.strptime(ls_de_use[i][2], '%Y/%m/%d %H:%M:%S.%f')).total_seconds() <= ls_de_use[i][3]):
                            mesID = irispy.classMethodObject("vital.measure", "%OpenId", str(j)).get("measureID")
                            mes_ls = get_IRISobj_ls_result("vital.measure", ls_de_use[i][0],j)
                            result_ls.append(mes_ls)
            
            pprint.pprint(result_ls)
    

    if q["バイタル名"] == "酸素飽和度":
            #パルスの機器ID取得　ls_deは二重配列
            ls_de = get_IRISobj_ls_DE("vital.DeviceEntry", "パルスオキシメーター", 1, 4)
            
            print(ls_de)
            #使用履歴の獲得　ls_de_useは二重配列
            ls_de_use = []
            for i in range(len(ls_de)):
                ls = get_IRISobj_ls_his("vital.history", q["患者番号"], ls_de[i][0], 1, maxID_his+1)
                for i in range(len(ls)):
                    ls_de_use.append(ls[i])

            print(ls_de_use)
            #イレギュラーチェック
            for i in range(len(ls_de_use)):
                period = check_irre_pa(maxID_his, ls_de_use[i])     
                ls_de_use[i].append(period)   

            print(ls_de_use)

            result_ls = []
            for i in range(len(ls_de_use)):
                for j in range(1, maxID_mea+1):
                    if irispy.classMethodValue("vital.measure", "existobject", j) == 1:
                        if ls_de_use[i][1] == irispy.classMethodObject("vital.measure", "%OpenId", str(j)).get("deviceID") and (0 <= (datetime.datetime.strptime(irispy.classMethodObject("vital.measure", "%OpenId", str(j)).get("Time"),'%Y/%m/%d %H:%M:%S.%f')  - datetime.datetime.strptime(ls_de_use[i][2], '%Y/%m/%d %H:%M:%S.%f')).total_seconds() <= ls_de_use[i][3]):
                            mesID = irispy.classMethodObject("vital.measure", "%OpenId", str(j)).get("measureID")
                            mes_ls = get_IRISobj_ls_result("vital.measure", ls_de_use[i][0],j)
                            result_ls.append(mes_ls)
            
            print(result_ls)
    # if q["Role"] == "血圧":
    #     ls_de = []
    #     for i in range(1, maxID+1):
    #         if irispy.classMethodValue("ion.bital", "existobject", i) == 1:
    #             entity = irispy.classMethodValue("ion.bital", "getEntity", i)
    #             role = irispy.classMethodValue("ion.bital", "getRole", i)
    #             if entity == "血圧計" and role == "機器ID":
    #                 ls_de.append(irispy.classMethodValue("ion.bital", "getDB", i))  #機器IDが入るはず
    #     print(ls_de)

    #     ls_de_use = []
    #     for i in range(len(ls_de)):
    #         for j in range(1,maxID+1):
    #             if irispy.classMethodValue("ion.bital", "existobject", j) == 1:
    #                 if ls_de[i] == irispy.classMethodValue("ion.bital", "getDB", j) and q["Entity"] == irispy.classMethodValue("ion.bital", "getEntity", j):  #機器IDそのものと患者IDが一致したら
    #                     ls_de_use.append([ls_de[i], irispy.classMethodValue("ion.bital", "getTemporal", j), j]) #機器IDと時間情報がセットの二重配列
    #     print(ls_de_use)

    #     for i in range(len(ls_de_use)):
    #         for j in range(1,maxID+1):
    #             if irispy.classMethodValue("ion.bital", "existobject", j) == 1 and irispy.classMethodValue("ion.bital", "getTemporal", j) != None:
    #                 #time_lim = datetime.datetime.strptime(irispy.classMethodValue("ion.bital", "getTemporal", j), '%Y/%m/%d %H:%M:%S.%f') - datetime.datetime.strptime(ls_de_use[i][1],'%Y/%m/%d %H:%M:%S.%f') 
    #                 time_all = datetime.datetime.strptime(irispy.classMethodValue("ion.bital", "getTemporal", j), '%Y/%m/%d %H:%M:%S.%f')
    #                 time_ls = datetime.datetime.strptime(ls_de_use[i][1],'%Y/%m/%d %H:%M:%S.%f')
    #                 bp = irispy.classMethodValue("ion.bital", "getRole", j)
    #                 if ls_de_use[i][0] == irispy.classMethodValue("ion.bital", "getEntity", j) and ( bp == "diastole" or bp == "mean" or bp == "systole" ) and (0 <= (time_all-time_ls).total_seconds() <= period):
    #                     result = {"Entity" : q["Entity"], "Role" : bp, "DB" : irispy.classMethodValue("ion.bital", "getDB", j), "Temporal" : time_all}
                
    #                     print(result)                    

    # print(result_ls)
    # if q["Temporal"] != "any":
    #     for i in range(len(result_ls)):
    #         if q["Temporal"] in result_ls[i]["Temporal"].strftime('%Y/%m/%d %H:%M:%S.%f'):
    #             result_ls[i]["Temporal"] = result_ls[i]["Temporal"].strftime('%Y/%m/%d %H:%M:%S.%f')
    #             #print(result_ls[i])
    #             pprint.pprint(result_ls[i], width=80)
    conn.close()
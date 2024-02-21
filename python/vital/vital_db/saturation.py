import iris
import datetime
import pprint
import sys
import json

args = {'hostname':'192.168.11.3', 'port':1972,
    'namespace':'FS', 'username':'_SYSTEM', 'password':'bmi-2718'
}
conn = iris.connect(**args)
# Create an iris object
irispy = iris.createIRIS(conn)

def query(E, R, T):
    q = {"Entity" : E, "Role" : R, "Temporal" : T}

    return q

def get_IRISobj_ls(cls, R, E, BE, DB, T, S, start, end):  
    ls_obj = []
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            if (R == obj.get("Role") or R == None) and (E == obj.get("Entity") or E == None) and (BE == obj.get("baseEntity") or BE == None) and (DB == obj.get("databody") or DB == None) and (T == obj.get("Temporal") or T == None) and (S == obj.get("Spatical") or S == None):
                ls_obj.append([obj.get("Role"), obj.get("Entity"), obj.get("baseEntity"), obj.get("databody"), obj.get("Temporal"), obj.get("Spatical")])

    return ls_obj

def get_IRISobj_dic(cls, R, E, BE, DB, T, S, start, end):  
    ls_obj_dic = []
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            if (R == obj.get("Role") or R == None) and (E == obj.get("Entity") or E == None) and (BE == obj.get("baseEntity") or BE == None) and (DB == obj.get("databody") or DB == None) and (T == obj.get("Temporal") or T == None) and (S == obj.get("Spatical") or S == None):
                ls_obj_dic.append({"Role": obj.get("Role"), "Entity":obj.get("Entity"), "Base Entity": obj.get("baseEntity"), "Data Body":obj.get("databody"), "Temporal":obj.get("Temporal"), "Spatical":obj.get("Spatical"), "Property": obj.get("propety")})

    return ls_obj_dic


def check_irre_pa(maxID,useDN):
    time = datetime.datetime.strptime(useDN["Temporal"],'%Y/%m/%d %H:%M:%S.%f')
    time_duration = time + datetime.timedelta(minutes=10)
    period = 600
    obj_ls = get_IRISobj_dic(cls="ion.bital", R="機器ID", E=None, BE=None, DB=None, T=None, S=None, start=1, end=(maxID+1))
    for i in range(len(obj_ls)):
        if ("PID" in obj_ls[i]["Entity"]) and useDN["Data Body"] == obj_ls[i]["Data Body"] and (time < datetime.datetime.strptime((obj_ls[i]["Temporal"]), '%Y/%m/%d %H:%M:%S.%f') < time_duration):
                diff = datetime.datetime.strptime(obj_ls[i]["Temporal"], '%Y/%m/%d %H:%M:%S.%f') - time
                period = diff.total_seconds()

    return period
                                                
                                    



if __name__ == '__main__':



    #クエリ作成
    q = json.loads(sys.argv[1])
    #print(q)
    #IRIS内の最大IDを取得
    maxID = irispy.classMethodValue("ion.bital", "getmaxID")
    #患者間での測定の最低時間
    period = 600

    #自動入力の流れ
    if q["Role"] == "saturation":
            
            ls_de = get_IRISobj_ls(cls="ion.bital", R="機器ID", E="パルスオキシメーター", BE=None, DB=None, T=None, S=None, start=1, end=(maxID+1))

            #print(ls_de)
            
            #ある患者（目的の患者）の使用履歴の獲得
            for  i in range(len(ls_de)):
                ls_de_use = get_IRISobj_dic("ion.bital", "機器ID", E=q["Entity"],BE=None, DB=ls_de[i][3],T=None, S=None, start=1, end=(maxID+1))
            
            #print(ls_de_use)

            #イレギュラーの確認
            for i in range(len(ls_de_use)):
                period = check_irre_pa(maxID, ls_de_use[i])     
                ls_de_use[i]["period"] = (period)       
            
            #print(ls_de_use)

            #バイタル獲得
            for i in range(len(ls_de)):
                ls_all_bt = get_IRISobj_dic(cls="ion.bital", R="saturation", E=ls_de[i][3], BE=None, DB=None, T=None, S=None, start=1, end=(maxID+1))

            #print(ls_all_bt)
            result_ls = []
            for i in range(len(ls_de_use)):
                for j in range(len(ls_all_bt)):
                    if ls_de_use[i]["Data Body"] == ls_all_bt[j]["Entity"] and (0 <= (datetime.datetime.strptime(ls_all_bt[j]["Temporal"], '%Y/%m/%d %H:%M:%S.%f')-datetime.datetime.strptime(ls_de_use[i]["Temporal"], '%Y/%m/%d %H:%M:%S.%f')).total_seconds() <= ls_de_use[i]["period"]):
                        result = {"Entity" : ls_de_use[i]["Entity"], "Role" : ls_all_bt[j]["Role"], "DataBody": ls_all_bt[j]["Data Body"],"Temporal" : ls_all_bt[j]["Temporal"] }
                        result_ls.append(result)
            print(result_ls)


    conn.close()
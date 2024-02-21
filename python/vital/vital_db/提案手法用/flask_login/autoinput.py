import irisnative
import datetime

ip = "192.168.0.67"
port = 1972
namespace = "FS"
username = "_SYSTEM"
password = "bmi-2718"

# create database connection and IRIS instance
connection = irisnative.createConnection(ip,port,namespace,username,password)
iris_native = irisnative.createIris(connection)

def query(E, R, T):
    q = {"Entity" : E, "Role" : R, "Temporal" : T}

    return q

def check_irre_pa(maxID,useDN):
    time = datetime.datetime.strptime(useDN[1],'%Y/%m/%d %H:%M:%S.%f')
    time_duration = time + datetime.timedelta(minutes=10)
    period = 600
    for i in range(1, maxID+1):
        if iris_native.classMethodValue("ion.bital", "existobject", i) == 1:
            if ( "PID" in iris_native.classMethodValue("ion.bital", "getEntity", i)) and iris_native.classMethodValue("ion.bital", "getDB", i) == useDN[0] and (time < datetime.datetime.strptime(iris_native.classMethodValue("ion.bital", "getTemporal", i), '%Y/%m/%d %H:%M:%S.%f') < time_duration):
                diff = datetime.datetime.strptime(iris_native.classMethodValue("ion.bital", "getTemporal", i), '%Y/%m/%d %H:%M:%S.%f') - time
                period = diff.total_seconds()
            else:
                continue
    
    return period
                                                
                                    



if __name__ == '__main__':



    #クエリ作成
    q = query("PID001", "酸素飽和度", datetime.date.today())

    #IRIS内の最大IDを取得
    maxID = iris_native.classMethodValue("ion.bital", "getmaxID")
    #患者間での測定の最低時間
    period = 600

    #自動入力の流れ
    if q["Role"] == "体温":
        ls_de = []
        for i in range(1, maxID+1):
            if iris_native.classMethodValue("ion.bital", "existobject", i) == 1:
                entity = iris_native.classMethodValue("ion.bital", "getEntity", i)
                role = iris_native.classMethodValue("ion.bital", "getRole", i)
                if entity == "体温計" and role == "機器ID":
                    ls_de.append(iris_native.classMethodValue("ion.bital", "getDB", i))  #機器IDが入るはず
        print(ls_de)
        ls_de_use = []
        for i in range(len(ls_de)):
            for j in range(1,maxID+1):
                if iris_native.classMethodValue("ion.bital", "existobject", j) == 1:
                    if ls_de[i] == iris_native.classMethodValue("ion.bital", "getDB", j) and q["Entity"] == iris_native.classMethodValue("ion.bital", "getEntity", j):  #機器IDそのものと患者IDが一致したら
                        ls_de_use.append([ls_de[i], iris_native.classMethodValue("ion.bital", "getTemporal", j), j]) #機器IDとPIDが使った時間情報がセットの二重配列
        #print(ls_de_use)

        for i in range(len(ls_de_use)):
            period = check_irre_pa(maxID, ls_de_use[i])     
            ls_de_use[i].append(period)       
        
        print(ls_de_use)
        for i in range(len(ls_de_use)):
            for j in range(1,maxID+1):
                if iris_native.classMethodValue("ion.bital", "existobject", j) == 1 and iris_native.classMethodValue("ion.bital", "getTemporal", j) != None:
                    #time_lim = datetime.datetime.strptime(iris_native.classMethodValue("ion.bital", "getTemporal", j), '%Y/%m/%d %H:%M:%S.%f') - datetime.datetime.strptime(ls_de_use[i][1],'%Y/%m/%d %H:%M:%S.%f')
                    time_all = datetime.datetime.strptime(iris_native.classMethodValue("ion.bital", "getTemporal", j), '%Y/%m/%d %H:%M:%S.%f')
                    time_ls = datetime.datetime.strptime(ls_de_use[i][1],'%Y/%m/%d %H:%M:%S.%f')
                    if ls_de_use[i][0] == iris_native.classMethodValue("ion.bital", "getEntity", j) and iris_native.classMethodValue("ion.bital", "getRole", j) == "bodytempurture" and (0 <= (time_all-time_ls).total_seconds() <= ls_de_use[i][3]):
                        result = {"Entity" : q["Entity"], "Role" : q["Role"], "DB" : iris_native.classMethodValue("ion.bital", "getDB", j), "Temporal" : time_all}
                
                        print(result)
                    else:
                        continue


    if q["Role"] == "酸素飽和度":
            ls_de = []
            for i in range(1, maxID+1):
                if iris_native.classMethodValue("ion.bital", "existobject", i) == 1:
                    entity = iris_native.classMethodValue("ion.bital", "getEntity", i)
                    role = iris_native.classMethodValue("ion.bital", "getRole", i)
                    if entity == "パルスオキシメーター" and role == "機器ID":
                        ls_de.append(iris_native.classMethodValue("ion.bital", "getDB", i))  #機器IDが入るはず
            print(ls_de)
            ls_de_use = []
            for i in range(len(ls_de)):
                for j in range(1,maxID+1):
                    if iris_native.classMethodValue("ion.bital", "existobject", j) == 1:
                        if ls_de[i] == iris_native.classMethodValue("ion.bital", "getDB", j) and q["Entity"] == iris_native.classMethodValue("ion.bital", "getEntity", j):  #機器IDそのものと患者IDが一致したら
                            ls_de_use.append([ls_de[i], iris_native.classMethodValue("ion.bital", "getTemporal", j), j]) #機器IDとPIDが使った時間情報がセットの二重配列
            print(ls_de_use)

            for i in range(len(ls_de_use)):
                period = check_irre_pa(maxID, ls_de_use[i])     
                ls_de_use[i].append(period)   

            print(ls_de_use)
            for i in range(len(ls_de_use)):
                for j in range(1,maxID+1):
                    if iris_native.classMethodValue("ion.bital", "existobject", j) == 1 and iris_native.classMethodValue("ion.bital", "getTemporal", j) != None:
                        #time_lim = datetime.datetime.strptime(iris_native.classMethodValue("ion.bital", "getTemporal", j), '%Y/%m/%d %H:%M:%S.%f') - datetime.datetime.strptime(ls_de_use[i][1],'%Y/%m/%d %H:%M:%S.%f')
                        time_all = datetime.datetime.strptime(iris_native.classMethodValue("ion.bital", "getTemporal", j), '%Y/%m/%d %H:%M:%S.%f')
                        time_ls = datetime.datetime.strptime(ls_de_use[i][1],'%Y/%m/%d %H:%M:%S.%f')
                        if ls_de_use[i][0] == iris_native.classMethodValue("ion.bital", "getEntity", j) and iris_native.classMethodValue("ion.bital", "getRole", j) == "saturation" and (0 <= (time_all-time_ls).total_seconds() <= ls_de_use[i][3]):
                            #q["Temporal"] == datetime.datetime.strptime(iris_native.classMethodValue("ion.bital", "getTemporal", j), '%Y/%m/%d %H:%M:%S.%f').date():　クエリーとの一致用
                            result = {"Entity" : q["Entity"], "Role" : q["Role"], "DB" : iris_native.classMethodValue("ion.bital", "getDB", j), "Temporal" : time_all}
                    
                            print(result)

    if q["Role"] == "血圧":
        ls_de = []
        for i in range(1, maxID+1):
            if iris_native.classMethodValue("ion.bital", "existobject", i) == 1:
                entity = iris_native.classMethodValue("ion.bital", "getEntity", i)
                role = iris_native.classMethodValue("ion.bital", "getRole", i)
                if entity == "血圧計" and role == "機器ID":
                    ls_de.append(iris_native.classMethodValue("ion.bital", "getDB", i))  #機器IDが入るはず
        print(ls_de)

        ls_de_use = []
        for i in range(len(ls_de)):
            for j in range(1,maxID+1):
                if iris_native.classMethodValue("ion.bital", "existobject", j) == 1:
                    if ls_de[i] == iris_native.classMethodValue("ion.bital", "getDB", j) and q["Entity"] == iris_native.classMethodValue("ion.bital", "getEntity", j):  #機器IDそのものと患者IDが一致したら
                        ls_de_use.append([ls_de[i], iris_native.classMethodValue("ion.bital", "getTemporal", j), j]) #機器IDと時間情報がセットの二重配列
        print(ls_de_use)

        for i in range(len(ls_de_use)):
            for j in range(1,maxID+1):
                if iris_native.classMethodValue("ion.bital", "existobject", j) == 1 and iris_native.classMethodValue("ion.bital", "getTemporal", j) != None:
                    #time_lim = datetime.datetime.strptime(iris_native.classMethodValue("ion.bital", "getTemporal", j), '%Y/%m/%d %H:%M:%S.%f') - datetime.datetime.strptime(ls_de_use[i][1],'%Y/%m/%d %H:%M:%S.%f') 
                    time_all = datetime.datetime.strptime(iris_native.classMethodValue("ion.bital", "getTemporal", j), '%Y/%m/%d %H:%M:%S.%f')
                    time_ls = datetime.datetime.strptime(ls_de_use[i][1],'%Y/%m/%d %H:%M:%S.%f')
                    bp = iris_native.classMethodValue("ion.bital", "getRole", j)
                    if ls_de_use[i][0] == iris_native.classMethodValue("ion.bital", "getEntity", j) and ( bp == "diastole" or bp == "mean" or bp == "systole" ) and (0 <= (time_all-time_ls).total_seconds() <= period):
                        result = {"Entity" : q["Entity"], "Role" : bp, "DB" : iris_native.classMethodValue("ion.bital", "getDB", j), "Temporal" : time_all}
                
                        print(result)                    

    connection.close()
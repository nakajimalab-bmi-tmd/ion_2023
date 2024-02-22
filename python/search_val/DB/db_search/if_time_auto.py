import iris
import csv
import json
import base64
import pprint
import subprocess
import ast
import xml.etree.ElementTree as ET
from xml.dom import minidom
import time

args = {'hostname':'192.168.11.3', 'port':1972,
    'namespace':'FS', 'username':'_SYSTEM', 'password':'bmi-2718'
    }
conn = iris.connect(**args)
# Create an iris object
irispy = iris.createIRIS(conn)


#get data of an object from IRIS. num is the ID of an object.
def getdata_iris(num):
    Role = irispy.classMethodValue("FS.if5","getRole", str(num))
    DataBody = irispy.classMethodValue("FS.if5","getDB", str(num))
    Entity = irispy.classMethodValue("FS.if5","getEntity", str(num))
    BaseEntity = irispy.classMethodValue("FS.if5","getBE", str(num))
    Temporal = irispy.classMethodValue("FS.if5","getTemporal", str(num))
    Spatical = irispy.classMethodValue("FS.if5","getSpatical", str(num))

    return Role, DataBody, Entity, BaseEntity, Temporal, Spatical

#delete object in IRIS. num is the ID of an object.
def delete_ID(num):

    delete = irispy.classMethodValue("FS.if5","delobject",str(num))

    return delete

#insert data of new object in IRIS. 
def insert(Role, Entity, BaseEntity, DataBody, Temporal, Spatical, Property):

    input = irispy.classMethodValue("FS.if5","Insert",Role, Entity, BaseEntity, DataBody, Temporal, Spatical, Property)

#confirm existance of an object. num is the ID of an object. if exist_object == 1, the ID of  object exists. if exist_object == 0, there is no ID object.
def exist_ID(num):

    exist_object = irispy.classMethodValue("FS.if5","existobject",str(num))

    return exist_object

def connect_iris(ip, port, ns, un, pw):

    connection = iris.createConnection(ip,port,ns,un,pw)
    irispy = iris.createIRIS(connection)

#一つのリストしか獲得できない
def get_IRISList(cls, R, E, BE, T, S, start, end):

    IRISlist = irispy.classMethodIRISList(cls, "getallos", R, E, BE, T, S, start, end)
    ls_IRIS = [IRISlist.get(1), IRISlist.get(2), IRISlist.get(3), IRISlist.get(4), IRISlist.get(5), IRISlist.get(6),IRISlist.get(7)]

    return ls_IRIS

#get_IRISListでは一つしかできないから、複数のリストをできるようにした
def get_allIRISList(cls, R, E, BE, T, S, start, end):
    ls_iris = []
    while True:
        ls_tmp = get_IRISList("FS.if5", R, E, BE, T, S, start, end)
        if ls_tmp[6] == "":
            break
        ls_iris.append(ls_tmp[0:5])
        start = int(ls_tmp[6])+1


def get_IRISobj_ls(cls, R, E, BE, T, S, start, end):  
    ls_obj = []
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            if (R == obj.get("Role") or R == None) and (E == obj.get("Entity") or E == None) and (BE == obj.get("baseEntity") or BE == None) and (T == obj.get("Temporal") or T == None) and (S == obj.get("Spatical") or S == None):
                ls_obj.append([obj.get("Role"), obj.get("Entity"), obj.get("baseEntity"), obj.get("databody"), obj.get("Temporal"), obj.get("Spatical")])

    return ls_obj

def get_IRISobj_dic(cls, R, E, BE, T, S, start, end):  
    ls_obj_dic = []
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            if (R == obj.get("Role") or R == None) and (E == obj.get("Entity") or E == None) and (BE == obj.get("baseEntity") or BE == None) and (T == obj.get("Temporal") or T == None) and (S == obj.get("Spatical") or S == None):
                ls_obj_dic.append({"Role": obj.get("Role"), "Entity":obj.get("Entity"), "Base Entity": obj.get("baseEntity"), "Data Body":obj.get("databody"), "Temporal":obj.get("Temporal"), "Spatical":obj.get("Spatical"), "Property": obj.get("propety")})

    return ls_obj_dic

def insert_program(prg_name):
    with open(prg_name, "r") as prg:
        prd_data = prg.read()
    #string_data = base64.b64encode(prd_data).decode('utf-8')
    newinsert = irispy.classMethodValue("FS.if5","InsertNewpy","PID",None, None, prd_data[0:50000], None, None,  json.dumps({"property":"inaoka_program_sample"}))
    start = 50000
    step = 50000

    while start < len(prd_data):
        add = irispy.classMethodValue("FS.if5","InsertAddpy", prd_data[start:start+step], newinsert)
        start += step

def get_program_ID(cls, R, E, BE, T, S, P, start, end):  
    ls_obj_dic = []
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            if (str(obj.get("outRole")) in str(R) or obj.get("outRole") == None) and (str(obj.get("outEntity")) in str(E) or obj.get("outEntity") == None) and (str(obj.get("outBaseEntity")) in str(BE) or obj.get("outBaseEntity") == None) and (T == obj.get("outTemporal") or obj.get("outTemporal") == None) and (S == obj.get("outSpatical") or obj.get("outSpatical") == None) and (P == obj.get("outProperty") or obj.get("outProperty") == None):
                ls_obj_dic.append({"Role": R, "Entity":E, "Base Entity": BE,  "Temporal":T, "Spatical":S, "Property": obj.get("outProperty"), "ID" : i})

    return ls_obj_dic

def get_prgID_time(cls, R, E, BE, T, S, P, start, end):  
    sum_iftime = 0
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            s = time.time()
            if (str(obj.get("outRole")) in str(R) or obj.get("outRole") == "any") and (str(obj.get("outEntity")) in str(E) or obj.get("outEntity") == "any") and (str(obj.get("outBaseEntity")) in str(BE) or obj.get("outBaseEntity") == "any") and (T == obj.get("outTemporal") or obj.get("outTemporal") == "any") and (S == obj.get("outSpatical") or obj.get("outSpatical") == "any") and (P == obj.get("outProperty") or obj.get("outProperty") == "any"):
                msg = "ok"
                f = time.time()
                sum_iftime += (f-s)
                break
            else:
                f_else = time.time()
                sum_iftime += (f_else-s)
                
    return sum_iftime, i

def get_program(num):
    step = 600000
    pos = 1
    data = ""
    while True:
        chunk = irispy.classMethodValue("FS.if5","getprogrampy", str(num), step, pos)
        data += chunk
        if len(chunk) < step:
            break
        pos += step
    return data

def get_result_from_prg(ls_prg, q):
    result_ls = []
    for i in range(len(ls_prg)):
        ls_prg[i]["Data Body"] = get_program(ls_prg[i]["ID"])

        out_prg = 'output' + str(ls_prg[i]["ID"]) + '.py'
        with open(out_prg, 'w') as prg_file:
            prg_file.write(ls_prg[i]["Data Body"])
        res = subprocess.run(['python3', out_prg, json.dumps(q, ensure_ascii=False)], capture_output=True)
        print("return code: {}".format(res.returncode))
        print("captured stdout: {}".format(res.stdout))  # こんにちは
        print("captured stderr: {}".format(res.stderr))  # こんばんは
        #astによる変換
        ls_de_str = res.stdout.decode()      
        l = ast.literal_eval(ls_de_str)
        result_ls += l

    return result_ls





if __name__ == '__main__':
    #start = time.time()
    cls_name = "FS.if50"
    maxID_prg = irispy.classMethodValue(cls_name, "getmaxID")

    q = {"Role" : "015", "Entity" : "PID001", "BaseEntity" : "any", "Temporal" : "any", "Spatical" : "any", "Property" : json.dumps({"format": "inaoka_program_sample_semantic"})}
    count = 1
    while count < 11:
        
        ls_prg, i = get_prgID_time(cls=cls_name, R=q["Role"], E=q["Entity"], BE=q["BaseEntity"], T=q["Temporal"], S=q["Spatical"], P=q["Property"], start=1, end=(maxID_prg+1))

        #end = time.time()
        #print(i)
        print(ls_prg)
        time.sleep(5)
        count += 1
        
    
    conn.close()


    

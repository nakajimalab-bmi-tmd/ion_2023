import iris
import csv
import json

import subprocess
import ast
import sys
import time

args = {'hostname':'192.168.11.3', 'port':1972,
    'namespace':'FS', 'username':'_SYSTEM', 'password':'bmi-2718'
    }
conn = iris.connect(**args)
# Create an iris object
irispy = iris.createIRIS(conn)

#delete object in IRIS. num is the ID of an object.
def delete_ID(num):

    delete = irispy.classMethodValue("ion.sample","delobject",str(num))

    return delete

#confirm existance of an object. num is the ID of an object. if exist_object == 1, the ID of  object exists. if exist_object == 0, there is no ID object.
def exist_ID(num):

    exist_object = irispy.classMethodValue("ion.sample","existobject",str(num))

    return exist_object


#一つのリストしか獲得できない
def get_IRISList(cls, R, E, BE, T, S, start, end):

    IRISlist = irispy.classMethodIRISList(cls, "getallos", R, E, BE, T, S, start, end)
    ls_IRIS = [IRISlist.get(1), IRISlist.get(2), IRISlist.get(3), IRISlist.get(4), IRISlist.get(5), IRISlist.get(6),IRISlist.get(7)]

    return ls_IRIS

#get_IRISListでは一つしかできないから、複数のリストをできるようにした
def get_allIRISList(cls, R, E, BE, T, S, start, end):
    ls_iris = []
    while True:
        ls_tmp = get_IRISList(cls, R, E, BE, T, S, start, end)
        if ls_tmp[6] == "":
            break
        ls_iris.append(ls_tmp[0:5])
        start = int(ls_tmp[6])+1
    return ls_iris


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
                ls_obj_dic.append({"Role": obj.get("Role"), "Entity":obj.get("Entity"), "Base Entity": obj.get("baseEntity"), "Data Body":obj.get("databody"), "Temporal":obj.get("Temporal"), "Spatical":obj.get("Spatical"), "Property": obj.get("Property")})

    return ls_obj_dic

def get_program_ID(cls, R, E, BE, T, S, P, start, end):  
    ls_obj_dic = []
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            if (str(obj.get("outRole")) in str(R) or obj.get("outRole") == None) and (str(obj.get("outEntity")) in str(E) or obj.get("outEntity") == None) and (str(obj.get("outBaseEntity")) in str(BE) or obj.get("outBaseEntity") == None) and (T == obj.get("outTemporal") or obj.get("outTemporal") == None) and (S == obj.get("outSpatical") or obj.get("outSpatical") == None) and (P == obj.get("outProperty") or obj.get("outProperty") == "any"):
                ls_obj_dic.append({"Role": R, "Entity":E, "Base Entity": BE,  "Temporal":T, "Spatical":S, "Property": obj.get("outProperty"), "ID" : i})

    return ls_obj_dic

def get_prgID_time(cls, R, E, BE, T, S, P, start, end):  
    sum_iftime = 0
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            s = time.time()
            if (str(obj.get("outRole")) in str(R) or obj.get("outRole") == "any") and (str(obj.get("outEntity")) in str(E) or obj.get("outEntity") == "any") and (str(obj.get("outBaseEntity")) in str(BE) or obj.get("outBaseEntity") =="any") and (T == obj.get("outTemporal") or obj.get("outTemporal") == "any") and (S == obj.get("outSpatical") or obj.get("outSpatical") == "any" ) and (P == obj.get("outProperty") or obj.get("outProperty") == "any"):
                msg = "ok"
                f = time.time()
                sum_iftime += (f-s)
                break
            else:
                f_else = time.time()
                sum_iftime += (f_else - s)
    return sum_iftime, i

def get_program(num):
    step = 600000
    pos = 1
    data = ""
    while True:
        chunk = irispy.classMethodValue("FS.if40recursive","getprogrampy", str(num), step, pos)
        data += chunk
        if len(chunk) < step:
            break
        pos += step
    return data



def get_result_from_prg(ls_prg, q):
    result_ls = []
    for i in range(len(ls_prg)):
        ls_prg[i]["Data Body"] = get_program(ls_prg[i]["ID"])
        conn.close()

        out_prg = 'output' + str(ls_prg[i]["ID"]) + '.py'
        with open(out_prg, 'w') as prg_file:
            prg_file.write(ls_prg[i]["Data Body"])
        res = subprocess.run(['python3', out_prg, json.dumps(q, ensure_ascii=False)], capture_output=True)
       
        #astによる変換
        ls_de_str = res.stdout.decode()      
        l = ast.literal_eval(ls_de_str)
        result_ls += l

    return result_ls

if __name__ == '__main__':

    cls_name = "FS.if40recursive"
    maxID_prg = irispy.classMethodValue(cls_name, "getmaxID")

    q = {"Role" : "005", "Entity" : "PID001", "BaseEntity" : "any", "Temporal" : "any", "Spatical" : "any", "Property" : json.dumps({"format": "inaoka_program_sample_semantic"})}

    sum_time, i = get_prgID_time(cls=cls_name, R=q["Role"], E=q["Entity"], BE=q["BaseEntity"], T=q["Temporal"], S=q["Spatical"], P=q["Property"], start=41, end=(maxID_prg+1))
    time_dic = {str(i): sum_time}
    ls_prg = get_program_ID(cls=cls_name, R=q["Role"], E=q["Entity"], BE=q["BaseEntity"], T=q["Temporal"], S=q["Spatical"], P=q["Property"], start=41, end=(maxID_prg+1))

    result = get_result_from_prg(ls_prg, q)
    result.append(time_dic)
    print(result)






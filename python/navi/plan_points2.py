#server側

import socket
import time
import json
import iris
import sys
import random
import ipget
import datetime
import ast
import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
import cv2

args = {'hostname':'192.168.11.3', 'port':1972,
    'namespace':'FS', 'username':'_SYSTEM', 'password':'bmi-2718'
    }



#IRISデータ取得
def get_IRISobj_ls(cls, R, E, BE, DB, T, S, start, end):
	ls_obj = []
	for i in range(start, end):
		if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
			obj = irispy.classMethodObject(cls, "%OpenId", str(i))
			if (R == obj.get("Role") or R == None) and (E == obj.get("Entity") or E == None) and (BE == obj.get("baseEntity") or BE == None) and (DB == obj.get("databody") or DB == None) and (T == obj.get("Temporal") or T == None) and (S == obj.get("Spatical") or S == None):
				ls_obj.append([obj.get("Role"), obj.get("Entity"), obj.get("baseEntity"), obj.get("databody"), obj.get("Temporal"), obj.get("Spatical")])

	return ls_obj

def get_IRISobj_dic(cls, R, E, BE, DB, T, S, P, start, end):  
	ls_obj_dic = []
	for i in range(start, end):
		if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
			obj = irispy.classMethodObject(cls, "%OpenId", str(i))
			if (R == obj.get("Role") or R == "any") and (E == obj.get("Entity") or E == "any") and (BE == obj.get("baseEntity") or BE == "any") and (DB == obj.get("databody") or DB == "any") and (T in obj.get("Temporal") or T == "any") and (S in obj.get("Spatical") or S == "any"):
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

#クライアント側が相手を見つける処理
def UDP_broadcast(query_json):
    #broadcast address
    host = "255.255.255.255"
    port = 7000

    #UDP
    cli_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    cli_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    cli_socket.settimeout(0.5)
    start_time = time.time()
    while True:
        try:
            end_time = time.time()
            #10秒以上探して相手が見つからなかったら強制終了
            if (end_time-start_time) > 20:
                print("相手がいません")
                rec_data = None
                addr = None
                
            # クエリの呼びかけ
            cli_socket.sendto(query_json.encode(), (host, port))    
    
            rec_data, addr = cli_socket.recvfrom(1024)

            #相手が見つかる
            if json.loads(rec_data)["msg"] == "ok":
                cli_socket.close()
                break

        except socket.timeout: #接続できる相手がいるまで何回もUDPで NW全体に質問
            time.sleep(0.5)

    return rec_data, addr

#TCPでデータを受け取る側の処理
def TCP_data_rcv(addr, rec_data):
    while True:
        try: 
            #TCP
            clitcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clitcpsocket.connect((addr[0], json.loads(rec_data)["port"]))

            #目的データの受信
            obj_data = b""
            while True:
                chunk = clitcpsocket.recv(1024)
                if not chunk:
                    break
                obj_data += chunk
            break
        except ConnectionRefusedError:
            time.sleep(0.05)

    return obj_data

def draw_line(image, points, color, alpha):
    pt1 = points[0].ravel()
    pt2 = points[1].ravel()
    image_copy = image.copy()
    cv2.line(image_copy, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), color, 2, cv2.LINE_AA)
    if alpha == 1.0:
        rst = image_copy
    else:
        rst = cv2.addWeighted(image_copy, alpha, image, 1.0-alpha, 0.0)
    return rst

def projection(T_Camera_target, length, intrinsic):
    target_points = np.zeros([2,1,3])
    target_points[0,0,:] = np.matmul(T_Camera_target, np.array([0., 0., length[0], 1.0]).T)[0:3]
    print("始点",target_points[0,0,:])
    target_points[1,0,:] = np.matmul(T_Camera_target, np.array([0., 0., length[1], 1.0]).T)[0:3]
    image_points, J = cv2.projectPoints(target_points, np.zeros(3), np.zeros(3), intrinsic, np.zeros(4))
    return image_points

def get_data(num):
    step = 600000
    pos = 1
    data = ""
    while True:
        chunk = irispy.classMethodValue("ion.navi","getdatapy", str(num), step, pos)
        data += chunk
        if len(chunk) < step:
            break
        pos += step
    return data

def get_data_ID(cls, R, E, BE, T, S, P, start, end):  
    ls_obj_dic = []
    for i in range(start, end):
        if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
            obj = irispy.classMethodObject(cls, "%OpenId", str(i))
            if (str(obj.get("Role")) in str(R) or (obj.get("Role") == "any")) and (str(obj.get("Entity")) in str(E) or (obj.get("Entity") == "any")) and (str(obj.get("baseEntity")) in str(BE) or (obj.get("baseEntity") == "any")) and (T == obj.get("Temporal") or obj.get("Temporal") == "any") and (S == obj.get("Spatical") or obj.get("Spatical") == "any") and (P == obj.get("propety") or obj.get("propety") == "any"):
                ls_obj_dic.append({"Role": R, "Entity":E, "Base Entity": BE,  "Temporal":T, "Spatical":S, "Property": obj.get("propety"), "ID" : i})

    return ls_obj_dic

#main
#server側のクエリ（担当のクエリ）
ip = ipget.ipget()
tcp_host = ip.ipaddr("wlan0").replace("/24", "")


svr_q_dic = {"semantics" : {"entity": "PID", "baseentity" : "any", "role" : "plan_points2", "spatial" : "any", "temporal" : "any"}, "dataproperty": {"format": "inaoka_matrix"}}

shut_dic = {"semantics" : {"entity": "shutdown", "baseentity" : "shutdown", "role" : "shutdown", "spatial" : "shutdown", "temporal" : "shutdown"}, "dataproperty": {"format": "shutdown"}}

while True:
    #broadcast address（待受がわ）
    host = ""
    port = 7000

    #UDP
    sock_rcvudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock_rcvudp.bind((host, port))

    while True:
        # クエリを受信
        rcv_data, addr = sock_rcvudp.recvfrom(1024)  

        cli_dic = json.loads(rcv_data)

        #条件判定、適切なクエリであればTCPに移行
        if (svr_q_dic["semantics"]["role"] in cli_dic["semantics"]["role"] or svr_q_dic["semantics"]["role"] == "any") and (svr_q_dic["semantics"]["entity"] in cli_dic["semantics"]["entity"] or svr_q_dic["semantics"]["entity"] == "any") and (svr_q_dic["semantics"]["baseentity"] in cli_dic["semantics"]["baseentity"] or svr_q_dic["semantics"]["baseentity"] == "any") and (svr_q_dic["semantics"]["temporal"] == cli_dic["semantics"]["temporal"] or svr_q_dic["semantics"]["temporal"] == "any") and (svr_q_dic["semantics"]["spatial"] == cli_dic["semantics"]["spatial"] or svr_q_dic["semantics"]["spatial"] == "any") and (svr_q_dic["dataproperty"] == cli_dic["dataproperty"] or svr_q_dic["dataproperty"] == "any"):
            random_num = random.randint(1,500)
            tcp_port = port + random_num
            res_msg = json.dumps({"msg" : "ok", "port" : tcp_port})
            #res_msg = "ok"
            sock_rcvudp.sendto(res_msg.encode(),addr)
            sock_rcvudp.close()
            break

        elif cli_dic==shut_dic:
            print(cli_dic)
            sys.exit()
            break
	    
   
    while True:
        try:
            sock_tcp = socket.socket(socket.AF_INET)
            sock_tcp.bind((tcp_host, tcp_port))
            sock_tcp.listen()
            break
        except ConnectionRefusedError:
            time.sleep(0.05)
	    
    while True:
        client, addr_tcp = sock_tcp.accept()
        print("accept")
        #目的データの送信
        conn = iris.connect(**args)
        # Create an iris object
        irispy = iris.createIRIS(conn)
        maxID = irispy.classMethodValue("ion.navi", "getmaxID")

        cliq1 = cli_dic.copy()
        cliq1["semantics"]["role"] = "T_Camera_Plan2"
        
        
        port_data, addr_data = UDP_broadcast(json.dumps(cliq1, ensure_ascii=False))
        if json.loads(port_data)["msg"] == "ok":
			
            T_Camera_Plan2_bin = TCP_data_rcv(addr_data,port_data)
            T_Camera_Plan2_ls = json.loads(T_Camera_Plan2_bin)["T_Camera_Plans2"]
            T_Camera_Plan2_array = np.array(T_Camera_Plan2_ls)        
        
        #プランの長さを取得、DBがjson
        #plan_set = get_IRISobj_dic(cls="navi", R="plan-20230502-newdataset.json", E="plan", BE="polaris", T="2023/05/02", S="TMDU/nkjlab",P=json.dumps({"format": "inaoka_json"}))
        plan_set = get_data_ID(cls="ion.navi",R="plan-20230502-newdataset.json", E="plan", BE="polaris", T="2023/05/02", S="TMDU/nkjlab",P=json.dumps({"format": "inaoka_json"}), start=1, end=(maxID+1))
        data_plan_set = get_data(plan_set[0]["ID"])
        plan_set_dic = json.loads(data_plan_set)
        plan_length = np.array(plan_set_dic["length"])
        #camera_set = get_IRISobj_dic(cls="navi", R="camera.json", E="camera", BE="polaris", T="2023", S="TMDU/nkjlab",P=json.dumps({"format": "inaoka_json"}))
        camera_set = get_data_ID(cls="ion.navi",R="camera.json", E="camera", BE="polaris", T="2023", S="TMDU/nkjlab",P=json.dumps({"format": "inaoka_json"}), start=1, end=(maxID+1))
        data_camera_set = get_data(camera_set[0]["ID"])
        camera_set_dic = json.loads(data_camera_set)
        camera_intrinsic = np.array(camera_set_dic["intrinsic"]) #行列
        plan_points2 = projection(T_Camera_Plan2_array, plan_length, camera_intrinsic)#行列,<class 'numpy.ndarray'>
        
        plan_points2_json = json.dumps({"plan_points2" : plan_points2.tolist()})
        client.send(plan_points2_json.encode())
        conn.close()
        break
    
    client.close()
    sock_tcp.close()

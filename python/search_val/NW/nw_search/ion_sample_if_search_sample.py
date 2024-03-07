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



#IRISデータ取得
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

#クライアント側が相手を見つける処理
def UDP_broadcast(query_json):
    #broadcast address
    host = "255.255.255.255"
    port = 7000

    #UDP
    cli_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    cli_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    #TCP rcv
    ip = ipget.ipget()
    tcp_host = ip.ipaddr("wlan0").replace("/24", "")
    port_rcv = 6000
    rcv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rcv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    rcv_socket.bind((tcp_host, port_rcv))
    rcv_socket.listen()
    
    cli_socket.settimeout(0.5)
    rcv_socket.settimeout(0.5)	
    start_time = time.time()
    while True:
        try:
            
            # クエリの呼びかけ
            cli_socket.sendto(query_json.encode(), (host, port))    
            print(1)
            #rec_data, addr = cli_socket.recvfrom(1024)
            cli_sock, addr = rcv_socket.accept()
            rec_data = cli_sock.recv(1024)
            #相手が見つかる
            if json.loads(rec_data)["msg"] == "ok":
                cli_socket.close()
                rcv_socket.close()
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

#main
#server側のクエリ（担当のクエリ）
ip = ipget.ipget()
tcp_host = ip.ipaddr("wlan0").replace("/24", "")


svr_q_dic = {"semantics" : {"entity": "PID", "baseentity" : "any", "role" : "hhh", "spatial" : "any", "temporal" : "any"}, "dataproperty": {"format": "inaoka_program_sample_semantic"}}
cli_q_dic = {"semantics" : {"entity": "PID", "baseentity" : "any", "role" : "iii", "spatial" : "any", "temporal" : "any"}, "dataproperty": {"format": "inaoka_program_sample_semantic"}}

shut_dic = {"semantics" : {"entity": "shutdown", "baseentity" : "shutdown", "role" : "shutdown", "spatial" : "shutdown", "temporal" : "shutdown"}, "dataproperty": {"format": "shutdown"}}

while True:
    #broadcast address（待受がわ）
    host = ""
    port = 7000
    #UDP
    sock_rcvudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock_rcvudp.bind((host, port))
    
    #TCP by send port 
    send_port = 6000  #相手(クライアント)のポート番号
    socket_sendtcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

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
            sock_rcvudp.close()
	    #tcpで返答
            socket_sendtcp.connect((addr[0], send_port))
            socket_sendtcp.sendall(res_msg.encode())
            break

        elif cli_dic==shut_dic:
            print(cli_dic)
            sys.exit()
            break
	    
    socket_sendtcp.close()
    

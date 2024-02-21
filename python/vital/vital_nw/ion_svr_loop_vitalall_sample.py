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

args = {'hostname':'192.168.11.3', 'port':1972,
    'namespace':'FS', 'username':'_SYSTEM', 'password':'bmi-2718'
}
conn = iris.connect(**args)
# Create an iris object
irispy = iris.createIRIS(conn)

#IRISデータ取得
def get_IRISobj_ls(cls, R, E, BE, DB, T, S, start, end):
	ls_obj = []
	for i in range(start, end):
		if irispy.classMethodValue(cls, "existobject", str(i)) == 1:
			obj = irispy.classMethodObject(cls, "%OpenId", str(i))
			if (R == obj.get("Role") or R == None) and (E == obj.get("Entity") or E == None) and (BE == obj.get("baseEntity") or BE == None) and (DB == obj.get("databody") or DB == None) and (T == obj.get("Temporal") or T == None) and (S == obj.get("Spatical") or S == None):
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
def TCP_data_rcv(addr,rec_data):
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
svr_q_dic = {"semantics" : {"entity": "PID", "baseentity" : "any", "role" : "vital_all", "spatial" : "any", "temporal" : "any"}, "dataproperty": {"format": "inaoka_program_sample"}}

ip = ipget.ipget()
tcp_host = ip.ipaddr("wlan0").replace("/24", "")

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
        print(cli_dic)

        #条件判定、適切なクエリであればTCPに移行
        if (svr_q_dic["semantics"]["role"] in cli_dic["semantics"]["role"] or svr_q_dic["semantics"]["role"] == "any") and (svr_q_dic["semantics"]["entity"] in cli_dic["semantics"]["entity"] or svr_q_dic["semantics"]["entity"] == "any") and (svr_q_dic["semantics"]["baseentity"] in cli_dic["semantics"]["baseentity"] or svr_q_dic["semantics"]["baseentity"] == "any") and (svr_q_dic["semantics"]["temporal"] == cli_dic["semantics"]["temporal"] or svr_q_dic["semantics"]["temporal"] == "any") and (svr_q_dic["semantics"]["spatial"] == cli_dic["semantics"]["spatial"] or svr_q_dic["semantics"]["spatial"] == "any") and (svr_q_dic["dataproperty"] == cli_dic["dataproperty"] or svr_q_dic["dataproperty"] == "any"):
            print("correspond")
            random_num = random.randint(1,500)
            tcp_port = port + random_num
            res_msg = json.dumps({"msg" : "ok", "port" : tcp_port})
            sock_rcvudp.sendto(res_msg.encode(),addr)
            sock_rcvudp.close()
            break
    

    #TCPによるデータ送信
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
        
        maxID_vital = irispy.classMethodValue("ion.bital", "getmaxID")
        print(cli_dic)
        q_bt = cli_dic.copy()
        q_bt["semantics"]["role"] = "bodytemperature"
        
        #bt
        bt_ls = get_IRISobj_dic(cls="ion.bital", R=q_bt["semantics"]["role"], E=q_bt["semantics"]["entity"], BE=q_bt["semantics"]["baseentity"], T=q_bt["semantics"]["temporal"], S = q_bt["semantics"]["spatial"], start=1, end=(maxID_vital+1))
        print(q_bt)
        port_data_bt, addr_bt = UDP_broadcast(json.dumps(q_bt, ensure_ascii=False))
        if port_data_bt == None:
            print("No bt !")
            bt_prg_ls=[]
        else:
            bt_prg_bin = TCP_data_rcv(addr_bt, port_data_bt)
            bt_prg_str = bt_prg_bin.decode()
            bt_prg_ls = ast.literal_eval(bt_prg_str)
        
        bt_result = bt_ls+bt_prg_ls
        
        #sa
        q_sa = cli_dic.copy()
        q_sa["semantics"]["role"] = "saturation"
        
        sa_ls = get_IRISobj_dic(cls="ion.bital", R=q_sa["semantics"]["role"], E=q_sa["semantics"]["entity"], BE=q_sa["semantics"]["baseentity"], T=q_sa["semantics"]["temporal"], S = q_sa["semantics"]["spatial"], start=1, end=(maxID_vital+1))
        print(q_sa)
        port_data_sa, addr_sa = UDP_broadcast(json.dumps(q_sa, ensure_ascii=False))
        if port_data_sa == None:
            print("No sa !")
            sa_prg_ls = []
        else:
            sa_prg_bin = TCP_data_rcv(addr_sa, port_data_sa)
            sa_prg_str = sa_prg_bin.decode()
            sa_prg_ls = ast.literal_eval(sa_prg_str)
        
        sa_result = sa_ls+sa_prg_ls
        
        #bp
        q_bp = cli_dic.copy()
        q_bp["semantics"]["role"] = "bloodpressure"
        
        bp_ls = get_IRISobj_dic(cls="ion.bital", R=q_bp["semantics"]["role"], E=q_bp["semantics"]["entity"], BE=q_bp["semantics"]["baseentity"], T=q_bp["semantics"]["temporal"], S = q_bp["semantics"]["spatial"], start=1, end=(maxID_vital+1))
        print(q_bp)
        port_data_bp, addr_bp = UDP_broadcast(json.dumps(q_bp, ensure_ascii=False))
        if port_data_bp == None:
            print("No bp !")
            bp_prg_ls = []
        
        else:
            bp_prg_bin = TCP_data_rcv(addr_bp, port_data_bp)
            bp_prg_str = bp_prg_bin.decode()
            bp_prg_ls = ast.literal_eval(bp_prg_str)
        
        bp_result = bp_ls+bp_prg_ls
        
        #vital_all
        vital_all = bt_result+sa_result+bp_result
        
        client.send(str(vital_all).encode())
        break


    client.close()
    sock_tcp.close()

#server側

import socket
import time
import json
import iris
import sys
import ipget
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
            if (end_time-start_time) > 10:
                print("相手がいません")
                sys.exit()
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
#cli側のクエリ
query_dic = {"semantics" : {"entity": "PID001", "baseentity" : "any", "role" : "aaa", "spatial" : "any", "temporal" : "any"}, "dataproperty": {"format": "inaoka_program_sample_semantic"}}


#クエリのjson文字列化、これをNWに流す。
query_json = json.dumps(query_dic, ensure_ascii=False)



count_num = 0
host = "192.168.11.45"
port = 7080
#udp
#rcv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#rcv_socket.bind((host, port))

ip = ipget.ipget()
tcp_host = ip.ipaddr("wlan0").replace("/24", "")
port_rcv = 6000
rcv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rcv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rcv_socket.bind((tcp_host, port_rcv))
rcv_socket.listen()
c_rcv, addr = rcv_socket.accept()
while True:
    
    msg, addr = rcv_socket.recvfrom(1024)
    print(json.loads(msg)["port"])
   
    
    
    
   

    

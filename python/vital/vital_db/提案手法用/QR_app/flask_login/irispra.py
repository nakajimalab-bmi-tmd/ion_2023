#自動入力用の練習ファイル

import irisnative
import csv
import json
import base64

ip = "192.168.0.67"
port = 1972
namespace = "FS"
username = "_SYSTEM"
password = "bmi-2718"

# create database connection and IRIS instance
connection = irisnative.createConnection(ip,port,namespace,username,password)
iris_native = irisnative.createIris(connection)



#デバイスの登録
# insert = iris_native.classMethodValue("ion.bital", "Insert", "機器ID", "血圧計", None, "e8:4f:25:40:fc:a8", None, None, None)
# insert = iris_native.classMethodValue("ion.bital", "Insert", "機器ID","体温計" , None, "c4:ac:59:7b:4a:c9", None, None, None)
# insert = iris_native.classMethodValue("ion.bital", "Insert", "機器ID", "パルスオキシメーター", None, "a0:c9:a0:40:eb:f9", None, None, None)

#DBの中身削除
# for i in range(45,49):

#     delete = iris_native.classMethodValue("ion.bital", "delobject", str(i))

#json挿入の確認
# d = {"unit" : "℃"}
# j = json.dumps(d, ensure_ascii=False)
# insert = iris_native.classMethodValue("FS.person2", "jsoninsert", j, None)

#バイナリストリームの挿入
# with open("sam.png", "rb") as f:
#     a = f.read()

# string_data = base64.b64encode(a)
# print(string_data)

# insert_bin = iris_native.classMethodValue("FS.practice", "Insert", string_data)


connection.close()
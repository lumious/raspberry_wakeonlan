# -*- coding:utf-8 -*-
from flask import Flask,render_template,request,jsonify
import re
import socket
import struct

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wake', methods=['POST'])
def wake():
    response = {}

    try:
        mac = request.values.get('mac_addr')
        if mac == None:
            raise ValueError
        if not check_mac(mac):
            raise ValueError
        wake_on_lan(mac)
        response['code']=1
        response['message']='请求成功'

    except ValueError:
        response['code']=0
        response['message'] = '请输入正确的MAC地址'

    return jsonify(response)

# 检查mac地址
def check_mac(mac_addr):
    # 长度检查
    if len(mac_addr) == 12:
        pass
    elif len(mac_addr) == 17:
        mac_addr = mac_addr.replace(':', '')
    else:
        return False
    # 正则检查
    pattern = re.compile(r'[0-9A-Fa-f]{12}')
    result = pattern.match(mac_addr)
    if result is not None:
        return True
    else:
        return False

def wake_on_lan(mac):
    if len(mac) == 12:
        pass
    elif len(mac) == 17:
        macaddress = mac.replace(':', '')
    else:
        raise ValueError('mac地址有误')
    data = 'FFFFFFFFFFFF' + mac * 16
    byte_data = b''
    for i in range(0, len(data), 2):
        byte_dat = struct.pack('B', int(data[i: i + 2], 16))
        byte_data = byte_data + byte_dat
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(byte_data, ('255.255.255.255', 7))
    sock.close()


if __name__ == '__main__':
    app.run(debug=False,port=5000,host='0.0.0.0')

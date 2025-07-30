import subprocess
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


def run_nmap_scan(network):
    try:
        # 执行nmap扫描命令
        cmd = f"nmap -sn {network} | grep -E 'Nmap scan report|MAC Address'"
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )

        # 解析扫描结果
        lines = result.stdout.strip().split('\n')
        devices = []
        current_device = {}

        for line in lines:
            if line.startswith('Nmap scan report'):
                if current_device:
                    devices.append(current_device)
                ip = line.split('for ')[-1].strip()
                current_device = {'ip': ip}
            elif line.startswith('MAC Address'):
                mac_info = line.split('MAC Address: ')[-1].strip()
                mac_parts = mac_info.split(' ')
                mac = mac_parts[0]
                vendor = ' '.join(mac_parts[2:]) if len(mac_parts) > 2 else 'Unknown'
                current_device['mac'] = mac
                current_device['vendor'] = vendor

        if current_device:
            devices.append(current_device)

        return devices

    except subprocess.CalledProcessError as e:
        return {"error": f"扫描失败: {e.stderr}"}
    except Exception as e:
        return {"error": f"发生未知错误: {str(e)}"}


@app.route('/')
def index():
    return render_template('index.html')


# 定义一个路由，当访问/scan时，使用POST方法
@app.route('/scan', methods=['POST'])
def scan_network():
    # 获取请求中的json数据
    data = request.json
    # 获取请求中的network参数，如果没有则默认为192.168.1.0/24
    network = data.get('network', '192.168.1.0/24')
    # 运行nmap扫描
    devices = run_nmap_scan(network)
    # 返回扫描结果
    return jsonify(devices)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
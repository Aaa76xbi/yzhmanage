import requests
from Demos.FileSecurityTest import permissions_dir_inherit

def JHL_devices_mannage():
    login_url = 'https://webapi.nbiotyun.com/login/multipartAccount'  #登录
    select_changjia_url = 'https://webapi.nbiotyun.com/login/multipartAccountLogin'  # 选择供应商
    shebei_liest_url = 'https://webapi.nbiotyun.com/system/index/menuTree'  # 设备列表
    device_search_url = 'https://webapi.nbiotyun.com/device/deviceList'  #设备搜索
    huifu_device_status_url = 'https://webapi.nbiotyun.com/deviceState/enable'  #恢复设备使用状态
    jihuo_device_url = 'https://webapi.nbiotyun.com/deviceState/reset'  # 激活设备


    headers = {
        'Cache-Control': 'no-cache',
        'User-Agent': 'PostmanRuntime/7.43.4',
        'Accept': '*/*',
    }

    data = {
        'phonenumber': '17286367919',
        'password': 'WDaCw5xqM/FoJhKuC4q3OZ2IVeNd1mjuqcWCZ+UgQ9rbTMinvvzf3slpYNvuBlWs/6FOqsYLoKaCKfp07YLmCmWJkqrH6iJ/XMx2UUAB43tnemmFRszjEreKFiqfHR2VtBLIvr6cRRGcYvADm9jiuuzNBC8EZYyQl29Jjzm3GhE=',
        'clientFlag': '1',
        'phoneCode': '+86',
    }

    # 禁用代理（根据之前的错误信息）
    proxies = {
        'http': None,
        'https': None
    }

    # 创建会话对象
    session = requests.Session()

    response = session.post(login_url, data=data, headers=headers, proxies=proxies) #登录请求
    print(response.json())


    headers = {
        'Cache-Control': 'no-cache',
        'User-Agent': 'PostmanRuntime/7.43.4',
        'Accept': '*/*',
    }
    data2 = {
        'phonenumber': '17286367919',
        'password': 'WDaCw5xqM/FoJhKuC4q3OZ2IVeNd1mjuqcWCZ+UgQ9rbTMinvvzf3slpYNvuBlWs/6FOqsYLoKaCKfp07YLmCmWJkqrH6iJ/XMx2UUAB43tnemmFRszjEreKFiqfHR2VtBLIvr6cRRGcYvADm9jiuuzNBC8EZYyQl29Jjzm3GhE=',
        'clientFlag': '1',
        'phoneCode': '+86',
        'deptId': '735868'
    }
    select_response = session.post(select_changjia_url, data=data2, headers=headers, proxies=proxies) #选择供应商
    print(select_response.json())

    headers = {
        'Cache-Control': 'no-cache',
        'User-Agent': 'PostmanRuntime/7.43.4',
        'Accept': '*/*',
    }

    data3 = {
        'clientFlag': '1'
    }
    shebei_liest = session.post(shebei_liest_url, data=data3, headers=headers, proxies=proxies)
    print(shebei_liest.json())

    headers = {
        'Cache-Control': 'no-cache',
        'User-Agent': 'PostmanRuntime/7.43.4',
        'Accept': '*/*',
    }
    data4 = {
        "deviceImei": "860722078836069",
        "deptId": "",
        "deptIdList": "",
        "deviceBatchId": "",
        "deviceVersionId": "",
        "deviceType": "",
        "placeBuildingId": "",
        "floorName": "",
        "flagBuilding": "",
        "state": "",
        "testState": "",
        "flagRetail": "",
        "pageNum": 1,
        "pageSize": 15,
        "deptLimit": "",
        "placeRoomId": "",
        "firstShipment": "",
        "boxNum": "",
        "orderByColumn": "",
        "isAsc": "",
        "iccid": "",
        "usingStatus": "",
        "startTime": "",
        "endTime": ""
    }
    device_search = session.post(device_search_url, data=data4, headers=headers, proxies=proxies)

    stateName = device_search.json().get('rows')[0].get('stateName')# 激活状态
    usingStatusName = device_search.json().get('rows')[0].get('usingStatusName')#使用状态
    deviceTypeName = device_search.json().get('rows')[0].get('deviceTypeName')#设备类型名称
    deviceMakerName = device_search.json().get('rows')[0].get('deviceMakerName')#设备厂商
    # print(device_search.json().get('rows')[0].get('usingStatusName'))
    print(deviceMakerName)
    print(deviceTypeName)
    print(usingStatusName)
    print(stateName)

    if usingStatusName != '正常使用':
        headers = {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        }
        data5 = {
            'deviceImeiList': '860722078836069',
            'stateRemark': '设备恢复使用状态'
        }

        huifu_device_status = session.post(huifu_device_status_url, data=data5, headers=headers, proxies=proxies)
        print('设备回复使用状态成功！',huifu_device_status.json())
        if stateName != '正常':
            headers = {
                'Cache-Control': 'no-cache',
                'User-Agent': 'PostmanRuntime/7.43.4',
                'Accept': '*/*',
            }
            data5 = {
                'deviceImeiList': '860722078836069'
            }

            jihuo_device = session.post(jihuo_device_url, data=data5, headers=headers, proxies=proxies)
            print('设备激活成功！',jihuo_device.json())

            #登录益智慧管理平台-绑定设备
            print('3抵达益智慧管理平台-绑定设备')
            yzh_login_url = ''
        print('2抵达益智慧管理平台-绑定设备')
        yzh_login_url = ''
    print('1抵达益智慧管理平台-绑定设备')

    device_data = {
        '使用状态': usingStatusName,
        '激活状态':stateName,
        '设备厂商': deviceMakerName,
        '设备名称': deviceTypeName,
        '设备编号': '860722078836069'
    }
    return device_data


print(JHL_devices_mannage())


yzh_login_url = 'https://admin.11yzh.com/admin/login/index.html'
yzh_session = requests.session()
headers = {
    'Cache-Control': 'no-cache',
    'User-Agent': 'PostmanRuntime/7.43.4',
    'Accept': '*/*',
}
data = {
    'username': 'admin',
    'password': 'Yzh4000000126..',
    '__token__': 'FBpHxRgj4oskwlMv0SCPyzbKtUqQIJNWLXGnYATaef8cE15hidrVm2OuD7Z693',
    'vcord': ''
}
proxies = {
    'http': None,
    'https': None
}

response = yzh_session.post(yzh_login_url, data=data, headers=headers, proxies=proxies)
print(response.json())


# try:
#     # 使用会话发送登录请求
#     response = session.post(login_url, data=data, headers=headers, proxies=proxies)
#
#     # 检查响应状态码
#     response.raise_for_status()
#
#     # 打印登录响应
#     login_data = response.json()
#     print("登录成功!")
#     print(login_data)
#
#     # 示例：使用同一个会话继续访问需要登录权限的接口
#     # protected_url = 'https://webapi.nbiotyun.com/api/protected'
#     # protected_response = session.get(protected_url)
#     # print(protected_response.json())
#
# except requests.exceptions.HTTPError as http_err:
#     print(f'HTTP 错误发生: {http_err}')
#     print(f'响应内容: {response.text}')  # 打印详细错误信息
# except requests.exceptions.RequestException as req_err:
#     print(f'请求错误发生: {req_err}')
# except ValueError as json_err:
#     print(f'JSON 解析错误: {json_err}')
#     print(f'原始响应内容: {response.text}')
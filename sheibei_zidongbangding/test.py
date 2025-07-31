import requests
from config.config import JLHconfig,hmConfig
request_data = JLHconfig
hm_config = hmConfig


def JLH_devices_sousuo(devices_id):          ###精隆华设备搜索
    # 禁用代理（根据之前的错误信息）
    proxies = {
        'http': None,
        'https': None
    }
    session = requests.Session()

    data = request_data.login('').get('data')
    headers = request_data.login('').get('headers')
    response = session.post(JLHconfig.login_url, data=data, headers=headers, proxies=proxies) #登录请求

    data = request_data.select_gongyingshang('','735868').get('data')
    headers = request_data.select_gongyingshang('','735868').get('headers')
    select_response = session.post(JLHconfig.select_changjia_url, data=data, headers=headers, proxies=proxies)  # 选择供应商
    print(select_response.json())
    data = request_data.sousuo_device('',devices_id).get('data')
    headers = request_data.sousuo_device('',devices_id).get('headers')
    device_search = session.post(JLHconfig.device_search_url, data=data, headers=headers, proxies=proxies)#搜索设备

    stateName = device_search.json().get('rows')[0].get('stateName')# 激活状态
    usingStatusName = device_search.json().get('rows')[0].get('usingStatusName')#使用状态
    deviceTypeName = device_search.json().get('rows')[0].get('deviceTypeName')#设备类型名称
    deviceMakerName = device_search.json().get('rows')[0].get('deviceMakerName')#设备厂商
    # print(device_search.json().get('rows')[0].get('usingStatusName'))

    device_data = {
        '使用状态': usingStatusName,
        '激活状态':stateName,
        '设备厂商': deviceMakerName,
        '设备名称': deviceTypeName,
        '设备编号': '860722078836069'
    }
    return device_data


# print(JLH_devices_sousuo('860722078836069'))

def HM_devices_select(devices_id):
    # 禁用代理（根据之前的错误信息）
    proxies = {
        'http': None,
        'https': None
    }
    session = requests.Session()


    data = hm_config.login('','636250').get('data')
    headers = hm_config.login('','636250').get('headers')


    select_response = session.post(JLHconfig.select_changjia_url, data=data, headers=headers, proxies=proxies)  # 选择供应商

    date = hm_config.deviuces_sosuo('',devices_id).get('data')
    headers = hm_config.deviuces_sosuo('',devices_id).get('headers')
    response = session.post(request_data.hm_devices_sousuo_url, data=date, headers=headers, proxies=proxies)
    print(response.json())


HM_devices_select('860376061280676')



































def JHL_devices_mannage():

    # 禁用代理（根据之前的错误信息）
    proxies = {
        'http': None,
        'https': None
    }

    # 创建会话对象
    session = requests.Session()

    data = request_data.login('').get('data')
    headers = request_data.login('').get('headers')
    response = session.post(JLHconfig.login_url, data=data, headers=headers, proxies=proxies) #登录请求
    print(response.json())

    data = request_data.select_gongyingshang('').get('data')
    headers = request_data.select_gongyingshang('').get('headers')
    select_response = session.post(JLHconfig.select_changjia_url, data=data, headers=headers, proxies=proxies) #选择供应商
    print(select_response.json())

    data = request_data.devices_list('').get('data')
    headers = request_data.devices_list('').get('headers')
    shebei_liest = session.post(JLHconfig.shebei_liest_url, data=data, headers=headers, proxies=proxies)#设备列表
    print(shebei_liest.json())


    data = request_data.sousuo_device('').get('data')
    headers = request_data.sousuo_device('').get('headers')
    device_search = session.post(JLHconfig.device_search_url, data=data, headers=headers, proxies=proxies)#搜索设备

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
        data = request_data.device_status('').get('data')
        headers = request_data.device_status('').get('headers')
        huifu_device_status = session.post(JLHconfig.huifu_device_status_url, data=data, headers=headers, proxies=proxies)#设备恢复使用状态
        print('设备回复使用状态成功！',huifu_device_status.json())
        if stateName != '正常':

            data = request_data.devices_jihuo('').get('data')
            headers = request_data.devices_jihuo('').get('headers')
            jihuo_device = session.post(JLHconfig.jihuo_device_url, data=data, headers=headers, proxies=proxies)#复位设别的状态为：正常
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

# devices_bangding = JHL_devices_mannage()
# print(devices_bangding)





# yzh_login_url = 'https://admin.11yzh.com/admin/login/index.html'#登录
# JHL_devicesList_url = 'https://admin.11yzh.com/admin/deviceinnopronew/finder?page=1&limit=20'#精隆华设备列表
# JHL_devices_tongbu_url = 'https://admin.11yzh.com/admin/deviceinnopronew/_synupdate'  #设备同步
# JHL_devices_sousuo_url = 'https://admin.11yzh.com/admin/deviceinnopronew/finder?page=1&limit=20&name=860722078836069&use_id=&type_id=&status='#设备搜索
# YHZusers_sousuo_url = 'https://admin.11yzh.com/admin/cuserarchives/finder'#用户搜索
# JHl_devices_bangdingUESR_url = 'https://admin.11yzh.com/admin/devicecuser/create'#设备绑定用户
# daping_username_url = 'https://admin.11yzh.com/admin/datalogin/finder'#大屏账号列表
# yzh_session = requests.session()
#
# #查询大屏账号是否存在
# headers = {
#     "accept": "application/json, text/javascript, /; q=0.01",
#     "accept-encoding": "gzip, deflate, br, zstd",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "cookie": "PHPSESSID=1458fbe20c262a401f24ad02d42ec7c5",
#     "priority": "u=1, i",
#     "referer": "https://admin.11yzh.com/admin.html",
#     "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"Windows"',
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
#     "x-requested-with": "XMLHttpRequest"
#     }
# proxies = {
#     'http': None,
#     'https': None
# }
# response = yzh_session.get(daping_username_url, headers=headers, proxies=proxies)
# print('大屏账号列表',response.json().get('data'))
# daping_list =  response.json().get('data')
# for i in daping_list:
#     print(i)
#
# headers = {
#     "accept": "/",
#     "accept-encoding": "gzip, deflate, br, zstd",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "content-length": "0",
#     "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
#     "origin": "https://admin.11yzh.com",
#     "priority": "u=1, i",
#     "referer": "https://admin.11yzh.com/admin.html",
#     "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"Windows"',
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
#     "x-requested-with": "XMLHttpRequest"
# }
# data = {
#     'username': 'admin',
#     'password': 'Yzh4000000126..',
#     '__token__': 'FBpHxRgj4oskwlMv0SCPyzbKtUqQIJNWLXGnYATaef8cE15hidrVm2OuD7Z693',
#     'vcord': ''
# }
#
#
# response = yzh_session.post(yzh_login_url, data=data, headers=headers, proxies=proxies)
# print(response.json())
#
# #查询用户是否存在
# headers = {
#     "accept": "application/json, text/javascript, */*; q=0.01",
#     "accept-encoding": "gzip, deflate, br, zstd",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
#     "priority": "u=1, i",
#     "referer": "https://admin.11yzh.com/admin.html",
#     "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"Windows"',
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
# }
#
# data = {
#     "page": 1,
#     "limit": 20,
#     'status': 1,
#     'name': '赵德柱',
# }
# response = yzh_session.post(YHZusers_sousuo_url, data=data, headers=headers, proxies=proxies)
# user_list = response.json().get('data')
# print('用户列表是：',user_list)
# print(user_list[0].get('id'))
# user_id = user_list[0].get('id')
# # print('判断用户是否存在',response.json().get('data')[0].get('name'))
# if len(user_list) != 0:
#     print('用户已存在！','用户信息是：',response.json())
#
#     if devices_bangding.get('设备厂商') == '精隆华':
#         print('成功判断厂商为-精隆华。返回厂商：', devices_bangding.get('设备厂商'))
#         headers = {
#             "accept": "application/json, text/javascript, */*; q=0.01",
#             "accept-encoding": "gzip, deflate, br, zstd",
#             "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#             "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
#             "priority": "u=1, i",
#             "referer": "https://admin.11yzh.com/admin.html",
#             "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
#             "sec-ch-ua-mobile": "?0",
#             "sec-ch-ua-platform": '"Windows"',
#             "sec-fetch-dest": "empty",
#             "sec-fetch-mode": "cors",
#             "sec-fetch-site": "same-origin",
#             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
#             "x-requested-with": "XMLHttpRequest"
#         }
#         data = {
#             "page": 1,
#             "limit": 20,
#             "name": "860722078836069",
#             "use_id": "",
#             "type_id": "",
#             "status": ""
#         }
#         response = yzh_session.post(JHL_devices_sousuo_url, data=data, headers=headers, proxies=proxies)
#         device_id =  response.json().get('data')[0].get('device_id')
#         type_name = response.json().get('data')[0].get('type_name')
#         # print('设备id',response.json().get('data')[0].get('type_name'))
#         device_data = response.json().get('data')
#
#         if len(device_data) == 0:
#             print('设备未找到！正在执行设备同步.....')
#             response = yzh_session.post(JHL_devices_tongbu_url, headers=headers, proxies=proxies)
#             print(response.json())
#             response = yzh_session.post(JHL_devices_sousuo_url, data=data, headers=headers, proxies=proxies)
#             device_data = response.json().get('data')
#             if len(device_data) == 0:
#                 print('设备未找到！请检查IMEI号是否正确！')
#             else:
#                 print('设备已找到！', device_data.get('data'))
#         else:
#             print('设备已找到！', device_data)
#
#             headers = {
#                 "accept": "*/*",
#                 "accept-encoding": "gzip, deflate, br, zstd",
#                 "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#                 "content-length": "294",
#                 "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
#                 "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
#                 "origin": "https://admin.11yzh.com",
#                 "priority": "u=1, i",
#                 "referer": "https://admin.11yzh.com/admin.html",
#                 "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
#                 "sec-ch-ua-mobile": "?0",
#                 "sec-ch-ua-platform": '"Windows"',
#                 "sec-fetch-dest": "empty",
#                 "sec-fetch-mode": "cors",
#                 "sec-fetch-site": "same-origin",
#                 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
#                 "x-requested-with": "XMLHttpRequest"
#             }
#             data = {
#               "id": 0,
#               "archives_id": user_id,
#               "device_id": device_id,
#               "device_alias": type_name,
#               "install_location": "卧室",
#               "device_num": 0,
#               "is_service_salvage": 1,
#               "is_ereport": 0,
#               "status": 1,
#               "camera_device_sn": "",
#               "relation_sn": "",
#               "relation_type": 1,
#               "relation_time": 0,
#               "relation_interval_time": 0,
#               "contact_phone1": "",
#               "contact_phone2": "",
#               "contact_phone3": ""
#             }
#             response = yzh_session.post(JHl_devices_bangdingUESR_url, data=data, headers=headers, proxies=proxies)
#             msg = response.json().get('msg')
#             print(response.json().get('msg'))
#             if msg == '一个用户不能重复绑定相同的设备！':
#                 print('该设备已绑定！---->', response.json())
#             else:
#                 print('绑定成功！---->', response.json())
#
#
#         # response = yzh_session.get(JHL_devicesList_url, headers=headers, proxies=proxies)
#         # print(response.text)
# else:
#     print('用户不存在！请天添加用户健康档案后继续操作!')


















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
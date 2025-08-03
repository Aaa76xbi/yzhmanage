import requests
import time
import json
from config.config import JLHconfig, hmConfig
from tkinter import LabelFrame

request_data = JLHconfig()
import cv2
from tkinter import filedialog, Tk, Frame, Label, Entry, Button, Text, Scrollbar, messagebox, ttk, StringVar
import numpy as np
import pyttsx3
import threading
from datetime import datetime

# 确保中文显示正常
import matplotlib

matplotlib.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]

hm_config = hmConfig()

print('正在打开 益智慧设备绑定程序.......')


class JLH_caozuo:
    proxies = {
        'http': None,
        'https': None
    }

    def __init__(self):
        # 初始化session（实例化时自动执行）
        self.session = requests.Session()

        # 登录请求
        data = request_data.login().get('data')
        headers = request_data.login().get('headers')
        response = self.session.post(
            JLHconfig.login_url,
            data=data,
            headers=headers,
            proxies=JLH_caozuo.proxies
        )

        # 选择供应商
        data = request_data.select_gongyingshang('735868').get('data')
        headers = request_data.select_gongyingshang('735868').get('headers')
        select_response = self.session.post(
            JLHconfig.select_changjia_url,
            data=data,
            headers=headers,
            proxies=JLH_caozuo.proxies
        )
        if select_response.json().get('msg') == '操作成功':
            print('登陆成功！', select_response.json())
            log_message("精隆华平台登录成功")

    def JLH_devices_sousuo(self, devices_id):  ### 精隆华设备搜索
        log_message(f"开始搜索精隆华设备: {devices_id}")
        data = request_data.sousuo_device(devices_id).get('data')
        headers = request_data.sousuo_device(devices_id).get('headers')
        # 使用实例的session发送请求（self是正确的实例对象）
        device_search = self.session.post(
            JLHconfig.device_search_url,
            data=data,
            headers=headers,
            proxies=JLH_caozuo.proxies
        )

        # 容错处理：避免返回空数据导致索引错误
        rows = device_search.json().get('rows', [])
        if not rows:
            log_message(f"未找到设备数据: {devices_id}")
            return {"错误": "未找到设备数据"}

        row_data = rows[0]
        device_data = {
            '使用状态': row_data.get('usingStatusName'),
            '激活状态': row_data.get('stateName'),
            '设备厂商': row_data.get('deviceMakerName'),
            '设备名称': row_data.get('deviceTypeName'),
            '设备编号': devices_id
        }
        log_message(f"找到设备: {device_data}")
        return device_data

    def JHL_devices_huifushiyong(self, device_id):  # 精隆华设别恢复使用状态
        log_message(f"开始恢复设备使用状态: {device_id}")
        data = request_data.device_status(device_id).get('data')
        headers = request_data.device_status(device_id).get('headers')
        huifu_device_status = self.session.post(JLHconfig.huifu_device_status_url, data=data, headers=headers,
                                                proxies=JLH_caozuo.proxies)  # 设备恢复使用状态
        if huifu_device_status.json().get('msg') == '操作成功':
            log_message(f'设备恢复使用状态成功: {device_id}')
            return {'使用状态': '正常使用'}
        else:
            log_message(f'设备恢复使用状态失败: {huifu_device_status.json()}')
            return {'错误': huifu_device_status.json().get('msg')}

    def device_status_huifu(self, device_id):  # 精隆化设备复位状态
        log_message(f"开始激活设备: {device_id}")
        data = request_data.devices_jihuo(device_id).get('data')
        headers = request_data.devices_jihuo(device_id).get('headers')
        jihuo_device = self.session.post(JLHconfig.jihuo_device_url, data=data, headers=headers,
                                         proxies=JLH_caozuo.proxies)  # 复位设别的状态为：正常
        log_message(f'设备激活结果: {jihuo_device.json()}')
        if jihuo_device.json().get('msg') == '操作成功':
            return {'激活状态': '正常'}
        else:
            return {'错误': jihuo_device.json().get('msg')}

    def JLH_devices_add(self, device_id):
        log_message(f"开始添加精隆华设备: {device_id}")
        data = request_data.devices_add(device_id).get('data')
        headers = request_data.devices_add(device_id).get('headers')
        devices_add = self.session.post(JLHconfig.devices_add_url, data=data, headers=headers,
                                        proxies=JLH_caozuo.proxies)
        add_xinxi = devices_add.json()
        log_message(f'设备添加结果: {add_xinxi}')
        return add_xinxi


# 益智慧平台相关配置
yzh_login_url = 'https://admin.11yzh.com/admin/login/index.html'  # 登录
JHL_devicesList_url = 'https://admin.11yzh.com/admin/deviceinnopronew/finder?page=1&limit=20'  # 精隆华设备列表
JHL_devices_tongbu_url = 'https://admin.11yzh.com/admin/deviceinnopronew/_synupdate'  # 设备同步
JHL_devices_sousuo_url = 'https://admin.11yzh.com/admin/deviceinnopronew/finder?page=1&limit=20&name=860722078836069&use_id=&type_id=&status='  # 设备搜索
YHZusers_sousuo_url = 'https://admin.11yzh.com/admin/cuserarchives/finder'  # 用户搜索
JHl_devices_bangdingUESR_url = 'https://admin.11yzh.com/admin/devicecuser/create'  # 设备绑定用户
daping_username_url = 'https://admin.11yzh.com/admin/datalogin/finder'  # 大屏账号列表
yzh_session = requests.session()


# 登录益智慧平台
def login_yzh_platform():
    log_message("开始登录益智慧平台")
    headers = {
        "accept": "/",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-length": "0",
        "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
        "origin": "https://admin.11yzh.com",
        "priority": "u=1, i",
        "referer": "https://admin.11yzh.com/admin.html",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    data = {
        'username': 'admin',
        'password': 'Yzh4000000126..',
        '__token__': 'FBpHxRgj4oskwlMv0SCPyzbKtUqQIJNWLXGnYATaef8cE15hidrVm2OuD7Z693',
        'vcord': ''
    }

    response = yzh_session.post(yzh_login_url, data=data, headers=headers,
                                proxies={'http': None, 'https': None})  # 登录益智慧平台
    log_message(f"益智慧平台登录结果: {response.json()}")
    return response.json()


# 查询用户是否存在
def sousuo_user(username):
    log_message(f"搜索用户: {username}")
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
        "priority": "u=1, i",
        "referer": "https://admin.11yzh.com/admin.html",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
    }

    data = {
        "page": 1,
        "limit": 20,
        'status': 1,
        'name': username,
    }
    response = yzh_session.post(YHZusers_sousuo_url, data=data, headers=headers,
                                proxies={'http': None, 'https': None})  # 用户搜索
    user_list = response.json().get('data')

    if len(user_list) != 0:
        log_message(f'找到用户: {user_list[0].get("name")}')
        user_id = user_list[0].get('id')
        user_data = {
            '用户名': user_list[0].get('name'),
            '用户id': user_id,
        }
        return user_data
    else:
        log_message(f"没有找到用户: {username}")
        return f"没有用户：{username}，请为其添加健康档案！"


def hm_devices_sousuo(devices_id):
    log_message(f"搜索驰通达/夜狼设备: {devices_id}")
    devices_id = str(devices_id)
    hm_devices_url = f'https://admin.11yzh.com/admin/devicectdyun/finder?page=1&limit=20&name={devices_id}&use_id=&type_id=&status='

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cookie": "PHPSESSID=ca1eb5132e4e64fda77036854a7d2a63",
        "priority": "u=1, i",
        "referer": "https://admin.11yzh.com/admin.html",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }

    devices_sousuo = yzh_session.get(hm_devices_url, headers=headers, proxies={'http': None, 'https': None})
    devices_sousuo_jieguo = devices_sousuo.json()
    log_message(f"驰通达/夜狼设备搜索结果: {devices_sousuo_jieguo}")
    return devices_sousuo_jieguo


def hm_devices_tongbu_msql():
    log_message("开始同步驰通达/夜狼设备数据库")
    url = 'https://admin.11yzh.com/admin/devicectdyun/_synupdate'
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-length": "0",
        "cookie": "PHPSESSID=ca1eb5132e4e64fda77036854a7d2a63",
        "origin": "https://admin.11yzh.com",
        "priority": "u=1, i",
        "referer": "https://admin.11yzh.com/admin.html",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }

    tongbu = yzh_session.post(url, headers=headers, proxies={'http': None, 'https': None})
    tongbu_jieguuuo = tongbu.json()
    log_message(f"驰通达/夜狼设备数据库同步结果: {tongbu_jieguuuo}")
    return tongbu_jieguuuo


def devices_select(changshang_name, device_id):
    log_message(f"搜索{changshang_name}设备: {device_id}")
    if changshang_name == '精隆华' or changshang_name == '精华隆':
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
            "priority": "u=1, i",
            "referer": "https://admin.11yzh.com/admin.html",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "x-requested-with": "XMLHttpRequest"
        }
        data = {
            "page": 1,
            "limit": 20,
            "name": device_id,
            "use_id": "",
            "type_id": "",
            "status": ""
        }
        response = yzh_session.post(JHL_devices_sousuo_url, data=data, headers=headers,
                                    proxies={'http': None, 'https': None})
        log_message(f"精隆华设备搜索响应: {response.json()}")

        if len(response.json().get('data')) != 0:
            device_id = response.json().get('data')[0].get('device_id')
            type_name = response.json().get('data')[0].get('type_name')
            device_data = {
                '设备名称': type_name,
                '设备id': device_id,
            }
            log_message(f'找到{changshang_name}设备: {device_data}')
            return device_data
        else:
            log_message(f'{changshang_name}设备不存在，正在同步数据库......')
            JLH_devices_tongbu_mysql()
            time.sleep(1.2)
            return devices_select('精隆华', device_id)

    elif changshang_name == '爱奥乐':
        log_message('处理爱奥乐设备')
        aal_devices_add(device_id)
        time.sleep(1)
        device_data = aal_device_YZHshousuo(device_id)
        return device_data
    elif changshang_name in ['驰通达', '夜狼']:
        log_message(f'处理{changshang_name}设备')
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
            "priority": "u=1, i",
            "referer": "https://admin.11yzh.com/admin.html",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "x-requested-with": "XMLHttpRequest"
        }
        data = {
            "page": 1,
            "limit": 20,
            "name": device_id,
            "use_id": "",
            "type_id": "",
            "status": ""
        }

        response = hm_devices_sousuo(device_id)
        if len(response.get('data')) != 0:
            device_id = response.get('data')[0].get('device_id')
            type_name = response.get('data')[0].get('type_name')
            device_data = {
                '设备名称': type_name,
                '设备id': device_id,
            }
            log_message(f'找到{changshang_name}设备: {device_data}')
            return device_data
        else:
            log_message(f'{changshang_name}设备不存在，正在同步数据库......')
            hm_devices_tongbu_msql()
            time.sleep(1.2)
            return devices_select(changshang_name, device_id)


def JLH_devices_tongbu_mysql():
    log_message("开始同步精隆华设备数据库")
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
        "priority": "u=1, i",
        "referer": "https://admin.11yzh.com/admin.html",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }

    response = yzh_session.post(JHL_devices_tongbu_url, headers=headers, proxies={'http': None, 'https': None})
    tongbu_xinxi = response.json().get('msg')
    if tongbu_xinxi == '同步成功！':
        log_message('精隆华设备数据库同步成功！')
    else:
        log_message(f'精隆华设备数据库同步失败: {response.json()}')
    return response.json()


def devicces_bangding(user_id, device_id, type_name):
    log_message(f"开始绑定设备 {device_id} 到用户 {user_id}")
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-length": "294",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
        "origin": "https://admin.11yzh.com",
        "priority": "u=1, i",
        "referer": "https://admin.11yzh.com/admin.html",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    data = {
        "id": 0,
        "archives_id": user_id,
        "device_id": device_id,
        "device_alias": type_name,
        "install_location": "卧室",
        "device_num": 0,
        "is_service_salvage": 1,
        "is_ereport": 0,
        "status": 1,
        "camera_device_sn": "",
        "relation_sn": "",
        "relation_type": 1,
        "relation_time": 0,
        "relation_interval_time": 0,
        "contact_phone1": "",
        "contact_phone2": "",
        "contact_phone3": ""
    }

    response = yzh_session.post(JHl_devices_bangdingUESR_url, data=data, headers=headers,
                                proxies={'http': None, 'https': None})
    log_message(f"设备绑定结果: {response.json()}")
    msg = response.json().get('msg')
    if msg == '一个用户不能重复绑定相同的设备！':
        return msg
    else:
        return msg


def aal_devices_YZHadd(device_name, device_id):
    log_message(f"添加爱奥乐设备到益智慧平台: {device_id}")
    url = 'https://admin.11yzh.com/admin/devicegprss/create'
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-length": "294",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
        "origin": "https://admin.11yzh.com",
        "priority": "u=1, i",
        "referer": "https://admin.11yzh.com/admin.html",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    data = {
        "id": 0,
        "device_id": "",
        "code": device_id,
        "device_sn": device_id,
        "name": f"{device_name}仪",
        "alias": f"{device_name}仪",
        "is_rented": 1,
        "deposit_fee": "",
        "use_id": 1,
        "type_id": 9,
        "thumb": "",
        "factory_id": 3,
        "brand": "",
        "model": "",
        "version": "",
        "production_date": "",
        "warranty_period": "",
        "service_user": "",
        "service_tel": "",
        "param": "",
        "funct": "",
        "images": "",
        "remark": "",
        "category": 0,
        "did": "",
        "imsi": "",
        "iccid": "",
        "unit": "",
        "dep": ""
    }

    device_add = yzh_session.post(url, headers=headers, data=data)
    log_message(f"爱奥乐设备添加结果: {device_add.json()}")
    return device_add.json()


def aal_device_YZHshousuo(device_id):
    log_message(f"在益智慧平台搜索爱奥乐设备: {device_id}")
    url = f'https://admin.11yzh.com/admin/devicegprss/finder?page=1&limit=20&name={device_id}&use_id=&type_id=&zone_id=0&code=&province_code=&city_code=&area_code=&street_code=&village_code=&level=1'
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cookie": "PHPSESSID=ca1eb5132e4e64fda77036854a7d2a63",
        "priority": "u=1, i",
        "referer": "https://admin.11yzh.com/admin.html",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    try:
        sousuo = yzh_session.get(url, headers=headers, timeout=10)
        log_message(f"爱奥乐设备搜索响应状态码: {sousuo.status_code}")
        if sousuo.status_code == 200 and sousuo.json().get('data'):
            device_id = sousuo.json().get('data')[0].get('device_id')
            log_message(f"找到爱奥乐设备: {device_id}")
            return device_id
        else:
            log_message(f"未找到爱奥乐设备: {device_id}")
            return None
    except Exception as e:
        log_message(f"爱奥乐设备搜索出错: {str(e)}")
        return None


def HM_devices_select(devices_id):
    log_message(f"搜索HM设备: {devices_id}")
    # 禁用代理
    proxies = {
        'http': None,
        'https': None
    }
    session = requests.Session()

    data = hm_config.login('636250').get('data')
    headers = hm_config.login('636250').get('headers')

    select_response = session.post(JLHconfig.select_changjia_url, data=data, headers=headers, proxies=proxies)  # 选择供应商

    date = hm_config.deviuces_sosuo(devices_id).get('data')
    headers = hm_config.deviuces_sosuo(devices_id).get('headers')
    response = session.post(request_data.hm_devices_sousuo_url, data=date, headers=headers, proxies=proxies)
    devices = response.json().get('rows')

    if len(devices) == 0:
        log_message(f'未找到HM设备: {devices_id}')
        device_data = {
            '设备厂商': '',
            '设备名称': '',
            '设备编号': '',
            '设备状态': '',
            '设备使用状态': '',
        }
        return device_data
    else:
        log_message(f'找到HM设备: {devices[0].get("deviceImei")}')
        device_data = {
            '设备厂商': devices[0].get('deviceMakerName'),
            '设备名称': devices[0].get('deviceTypeName'),
            '设备编号': devices[0].get('deviceImei'),
            '设备状态': devices[0].get('stateName'),
            '设备使用状态': devices[0].get('usingStatusName'),
        }
        return device_data


def hm_devices_huifu_status(device_id):
    log_message(f"恢复HM设备状态: {device_id}")
    # 禁用代理
    proxies = {
        'http': None,
        'https': None
    }
    session = requests.Session()

    data = hm_config.login('636250').get('data')
    headers = hm_config.login('636250').get('headers')

    select_response = session.post(JLHconfig.select_changjia_url, data=data, headers=headers, proxies=proxies)  # 选择供应商

    date = hm_config.hm_devices_huifu(device_id).get('data')
    headers = hm_config.hm_devices_huifu(device_id).get('headers')
    response = session.post(request_data.hm_devices_huifushiyong_ul, data=date, headers=headers, proxies=proxies)
    log_message(f"HM设备状态恢复结果: {response.json()}")
    return response.json()


def HM_devices_add(device_id):
    log_message(f"添加HM设备: {device_id}")
    addurl = 'https://webapi.nbiotyun.com/device/add'

    # 禁用代理
    proxies = {
        'http': None,
        'https': None
    }
    session = requests.Session()

    data = hm_config.login('636250').get('data')
    headers = hm_config.login('636250').get('headers')

    select_response = session.post(JLHconfig.select_changjia_url, data=data, headers=headers, proxies=proxies)  # 选择供应商
    data = hm_config.hm_devices_add(device_id).get('data')
    headers = hm_config.hm_devices_add(device_id).get('headers')
    add_device = session.post(addurl, headers=headers, data=data, proxies=proxies)
    add_device_xinxi = add_device.json()
    log_message(f"HM设备添加结果: {add_device_xinxi}")
    return add_device_xinxi


def hm_devices_jihuo(device_id):
    log_message(f"激活HM设备: {device_id}")
    jihuo_url = 'https://webapi.nbiotyun.com/deviceState/reset'
    # 禁用代理
    proxies = {
        'http': None,
        'https': None
    }
    session = requests.Session()

    data = hm_config.login('636250').get('data')
    headers = hm_config.login('636250').get('headers')

    select_response = session.post(JLHconfig.select_changjia_url, data=data, headers=headers, proxies=proxies)  # 选择供应商
    data = hm_config.hm_devices_jihuo(device_id).get('data')
    headers = hm_config.hm_devices_jihuo(device_id).get('headers')
    jihuo_device = session.post(request_data.hm_devices_fuwei_url, headers=headers, data=data, proxies=proxies)
    fuwei_jieguo = jihuo_device.json()
    log_message(f"HM设备激活结果: {fuwei_jieguo}")
    return fuwei_jieguo


# 爱奥乐相关功能
aal_login_url = 'http://tf.ydjk5.com/gprs/login'  # 确认URL正确性
proxies = {'http': None, 'https': None}
data = {'username': "gzyzh", 'password': "gz123456"}

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/json",  # 声明JSON格式
    "host": "tf.ydjk5.com",
    "origin": "http://tf.ydjk5.com",
    "proxy-connection": "keep-alive",
    "referer": "http://tf.ydjk5.com/login",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    "x-requested-with": "XMLHttpRequest"
}

aal_sesson = requests.session()


# 登录爱奥乐平台
def login_aal_platform():
    log_message("开始登录爱奥乐平台")
    try:
        login = aal_sesson.post(
            aal_login_url,
            json=data,
            headers=headers,
            proxies=proxies
        )
        log_message(f"爱奥乐平台登录结果: {login.json()}")
        return login.json()
    except Exception as e:
        log_message(f"爱奥乐平台登录失败: {str(e)}")
        return None


def aal_devices_add(device_id):
    log_message(f"添加爱奥乐设备: {device_id}")
    url = 'http://tf.ydjk5.com/gprs/dev/rule/add'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/json",
        "host": "tf.ydjk5.com",
        "origin": "http://tf.ydjk5.com",
        "proxy-connection": "keep-alive",
        "referer": "http://tf.ydjk5.com/login",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    data = {
        "brandId": "f843e5c8-34a6-4a9d-9ff3-1b7c160a8acb",
        "deptId": "0f28de53-7506-46f8-868e-8f3a504a0ee1",
        "devicesModel": "3",
        "devicesSn": f"{device_id}###",
        "devicesType": "1",
        "transmitlFlag": "1",
        "userOneTransmitlFlag": "1",
        "userTwoTransmitlFlag": "1"
    }

    try:
        add_devices = aal_sesson.post(url, headers=headers, json=data)
        log_message(f"爱奥乐设备添加结果: {add_devices.json()}")
        return add_devices.json()
    except Exception as e:
        log_message(f"爱奥乐设备添加失败: {str(e)}")
        return None


def aal_ddevices_sousuo(device_id):
    log_message(f"搜索爱奥乐设备: {device_id}")
    url = 'http://tf.ydjk5.com/gprs/dev/rule/list'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/json",
        "host": "tf.ydjk5.com",
        "origin": "http://tf.ydjk5.com",
        "proxy-connection": "keep-alive",
        "referer": "http://tf.ydjk5.com/login",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    data = {'brandName': "", 'deptName': "", 'devSN': device_id, 'page': 1, 'rows': 10}
    try:
        device_sousuo = aal_sesson.post(url, headers=headers, json=data)
        if device_sousuo.json().get('data') and device_sousuo.json().get('data').get('list'):
            device_info = device_sousuo.json().get('data').get('list')[0]
            device_name = device_info.get('devicesTypeNum')
            device_id = device_info.get('devicesSn')
            devices_data = {
                '设备名称': device_name,
                '设备id': device_id,
                '设备厂商': '爱奥乐'
            }
            log_message(f"找到爱奥乐设备: {devices_data}")
            return devices_data
        else:
            log_message(f"未找到爱奥乐设备: {device_id}")
            return None
    except Exception as e:
        log_message(f"爱奥乐设备搜索失败: {str(e)}")
        return None


def simple_speak(text):
    log_message(f"语音播报: {text}")
    try:
        engine = pyttsx3.init()  # 初始化
        engine.say(text)  # 加入朗读内容
        engine.runAndWait()  # 执行朗读
    except Exception as e:
        log_message(f"语音播报失败: {str(e)}")


def decode_qrcode_from_image(image_path):
    """从图像路径读取并解码二维码的函数"""
    log_message(f"从图片解码二维码: {image_path}")
    try:
        image = cv2.imread(image_path)
        result, _ = detect_and_decode_strict(image)
        if result:
            log_message(f"二维码解码成功: {result}")
        else:
            log_message("未识别到二维码")
        return result
    except Exception as e:
        log_message(f"二维码解码失败: {str(e)}")
        return None


def select_image():
    """打开文件选择对话框选择图像的函数"""
    log_message("打开图片选择对话框")
    Tk().withdraw()
    file_path = filedialog.askopenfilename(title="选择图片",
                                           filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        try:
            image = cv2.imread(file_path)
            data, bbox = detect_and_decode_strict(image)
            if data:
                log_message(f"图片识别成功，解码内容: {data}")
                # 在界面上显示识别到的设备ID
                app.device_id_var.set(data)

                cv2.putText(image, f"{data}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                # 绘制二维码边框
                if bbox is not None and len(bbox) >= 4:
                    for i in range(4):
                        cv2.line(image, tuple(bbox[i]), tuple(bbox[(i + 1) % 4]), (255, 0, 0), 2)

                cv2.imshow("识别结果", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                log_message("图片中未识别到二维码")
                messagebox.showinfo("提示", "未识别到二维码")
        except Exception as e:
            log_message(f"图片处理失败: {str(e)}")
            messagebox.showerror("错误", f"处理图片时出错: {str(e)}")


def enhance_image(image):
    """增强图像质量以便更好地检测二维码的函数"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharp = cv2.filter2D(gray, -1, sharpen_kernel)
    return sharp


def detect_and_decode_strict(image):
    """严格检测和解码二维码的函数"""
    detector = cv2.QRCodeDetector()
    gray = enhance_image(image)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # 确保ROI区域足够大
        if w < 30 or h < 30:
            continue

        roi = image[y:y + h, x:x + w]

        # 检查ROI是否有效
        if roi.size == 0 or roi.shape[0] <= 0 or roi.shape[1] <= 0:
            continue

        try:
            # 尝试检测和解码二维码
            data, bbox, _ = detector.detectAndDecode(roi)
            if data:
                # 计算角点在原图中的坐标
                if bbox is not None and bbox.size > 0:
                    bbox = bbox.reshape(-1, 2).astype(int)
                    # 调整角点坐标到原图坐标系
                    for i in range(len(bbox)):
                        bbox[i][0] += x
                        bbox[i][1] += y
                    return data, bbox  # 返回数据和角点
                return data, None  # 没有角点信息时返回None
        except Exception as e:
            log_message(f"处理ROI时出错: {e}")
            continue  # 继续尝试其他轮廓

    return None, None  # 未检测到二维码


def scan_from_camera():
    log_message("启动摄像头扫码")
    cap = cv2.VideoCapture(0)
    result = None

    while True:
        ret, frame = cap.read()
        if not ret:
            log_message("无法获取摄像头画面，退出扫码")
            cap.release()
            cv2.destroyAllWindows()
            messagebox.showerror("错误", "无法获取摄像头画面")
            return None

        data, bbox = detect_and_decode_strict(frame)
        if data:
            result = data
            log_message(f"摄像头扫码成功，内容: {data}")
            # 在界面上显示识别到的设备ID
            app.device_id_var.set(data)

            # 生成语音文本
            try:
                jlh = JLH_caozuo()
                device_data = jlh.JLH_devices_sousuo(data)
                if device_data.get('设备厂商') is not None:
                    yuyin2_txt = f"厂商{device_data.get('设备厂商')},设备{device_data.get('设备名称')},使用状态{device_data.get('使用状态')},设备状态{device_data.get('激活状态')}，设备编号{device_data.get('设备编号')}"
                    simple_speak(yuyin2_txt)
            except Exception as e:
                log_message(f"获取设备信息失败: {str(e)}")

            # 绘制边框并显示
            cv2.putText(frame, f"{data}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            if bbox is not None and len(bbox) >= 4:
                for i in range(4):
                    cv2.line(frame, tuple(bbox[i]), tuple(bbox[(i + 1) % 4]), (255, 0, 0), 2)

            cv2.imshow("摄像头扫码", frame)
            cv2.waitKey(1000)
            break

        # 显示实时画面
        cv2.imshow("摄像头扫码 (按ESC退出)", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC键退出
            break

    cap.release()
    cv2.destroyAllWindows()
    return result


# 日志相关函数
def log_message(message):
    """添加日志消息到界面"""
    if hasattr(app, 'log_text'):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"

        # 在主线程中更新UI
        app.log_text.config(state="normal")
        app.log_text.insert("end", log_entry)
        app.log_text.see("end")
        app.log_text.config(state="disabled")


# 界面类
class DeviceBindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("益智慧设备绑定程序")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)

        # 创建主框架
        main_frame = Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 创建左侧功能区
        left_frame = Frame(main_frame, width=600)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # 设备操作区
        device_frame = LabelFrame(left_frame, text="设备操作", padx=10, pady=10)
        device_frame.pack(fill="x", pady=(0, 10))

        # 设备厂商选择
        Label(device_frame, text="设备厂商:").grid(row=0, column=0, sticky="w", pady=5)
        self.manufacturer_var = StringVar(value="精隆华")
        manufacturer_options = ["精隆华", "精华隆", "爱奥乐", "驰通达", "夜狼"]
        manufacturer_menu = ttk.Combobox(device_frame, textvariable=self.manufacturer_var, values=manufacturer_options,
                                         width=15)
        manufacturer_menu.grid(row=0, column=1, sticky="w", pady=5)

        # 设备ID输入
        Label(device_frame, text="设备ID:").grid(row=1, column=0, sticky="w", pady=5)
        self.device_id_var = StringVar()
        Entry(device_frame, textvariable=self.device_id_var, width=30).grid(row=1, column=1, sticky="w", pady=5)

        # 设备操作按钮
        device_btn_frame = Frame(device_frame)
        device_btn_frame.grid(row=1, column=2, columnspan=2, padx=10)

        Button(device_btn_frame, text="搜索设备", command=self.search_device).pack(side="left", padx=5)
        Button(device_btn_frame, text="恢复使用", command=self.restore_device).pack(side="left", padx=5)
        Button(device_btn_frame, text="激活设备", command=self.activate_device).pack(side="left", padx=5)
        Button(device_btn_frame, text="添加设备", command=self.add_device).pack(side="left", padx=5)

        # 二维码扫描区
        qrcode_frame = LabelFrame(left_frame, text="二维码扫描", padx=10, pady=10)
        qrcode_frame.pack(fill="x", pady=(0, 10))

        Button(qrcode_frame, text="选择图片扫码", command=self.run_select_image).pack(side="left", padx=10, pady=5)
        Button(qrcode_frame, text="摄像头扫码", command=self.run_scan_camera).pack(side="left", padx=10, pady=5)

        # 用户操作区
        user_frame = LabelFrame(left_frame, text="用户操作", padx=10, pady=10)
        user_frame.pack(fill="x", pady=(0, 10))

        Label(user_frame, text="用户名:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_var = StringVar()
        Entry(user_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, sticky="w", pady=5)
        # Button(user_frame, text="搜索用户", command=self.search_user).pack(row=0, column=2, padx=10, pady=5)
        Button(user_frame, text="搜索用户", command=self.search_user).grid(row=0, column=2, padx=10, pady=5)

        # 绑定信息显示
        self.user_info_var = StringVar(value="未搜索到用户")
        Label(user_frame, textvariable=self.user_info_var).grid(row=1, column=0, columnspan=3, sticky="w", pady=5)

        # 绑定操作区
        binding_frame = LabelFrame(left_frame, text="设备绑定", padx=10, pady=10)
        binding_frame.pack(fill="x", pady=(0, 10))

        Button(binding_frame, text="绑定设备到用户", command=self.bind_device).pack(pady=5)

        # 设备信息显示区
        self.device_info_var = StringVar(value="设备信息将在这里显示")
        device_info_frame = LabelFrame(left_frame, text="设备信息", padx=10, pady=10)
        device_info_frame.pack(fill="both", expand=True)
        Label(device_info_frame, textvariable=self.device_info_var, justify="left", wraplength=500).pack(anchor="w")

        # 创建右侧日志区
        right_frame = Frame(main_frame, width=400)
        right_frame.pack(side="right", fill="both", expand=True)

        log_frame = LabelFrame(right_frame, text="操作日志", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True)

        # 日志文本框和滚动条
        log_scrollbar = Scrollbar(log_frame)
        log_scrollbar.pack(side="right", fill="y")

        self.log_text = Text(log_frame, wrap="word", state="disabled", yscrollcommand=log_scrollbar.set)
        self.log_text.pack(fill="both", expand=True)
        log_scrollbar.config(command=self.log_text.yview)

        # 存储临时数据
        self.current_user_id = None
        self.current_device_data = None

        # 初始化连接
        self.init_connections()

    def init_connections(self):
        """初始化平台连接"""

        def init():
            log_message("初始化平台连接...")
            # 登录精隆华
            try:
                global jlh_instance
                jlh_instance = JLH_caozuo()
            except Exception as e:
                log_message(f"精隆华平台初始化失败: {str(e)}")

            # 登录益智慧
            try:
                login_yzh_platform()
            except Exception as e:
                log_message(f"益智慧平台登录失败: {str(e)}")

            # 登录爱奥乐
            try:
                login_aal_platform()
            except Exception as e:
                log_message(f"爱奥乐平台登录失败: {str(e)}")

            log_message("初始化完成")

        # 在新线程中执行初始化，避免界面卡顿
        threading.Thread(target=init, daemon=True).start()

    def search_device(self):
        """搜索设备"""
        device_id = self.device_id_var.get().strip()
        manufacturer = self.manufacturer_var.get()

        if not device_id:
            messagebox.showwarning("警告", "请输入设备ID")
            return

        def search():
            log_message(f"开始搜索{manufacturer}设备: {device_id}")
            try:
                if manufacturer in ["精隆华", "精华隆"]:
                    result = jlh_instance.JLH_devices_sousuo(device_id)
                    self.current_device_data = result
                elif manufacturer == "爱奥乐":
                    result = aal_ddevices_sousuo(device_id)
                    self.current_device_data = result
                elif manufacturer in ["驰通达", "夜狼"]:
                    result = hm_devices_sousuo(device_id)
                    if result.get('data'):
                        self.current_device_data = result.get('data')[0]
                    else:
                        self.current_device_data = None
                else:
                    result = "不支持的厂商类型"

                # 显示设备信息
                if isinstance(result, dict):
                    info_text = "\n".join([f"{k}: {v}" for k, v in result.items()])
                else:
                    info_text = str(result)

                self.device_info_var.set(info_text)
            except Exception as e:
                log_message(f"搜索设备失败: {str(e)}")
                messagebox.showerror("错误", f"搜索设备失败: {str(e)}")

        threading.Thread(target=search, daemon=True).start()

    def restore_device(self):
        """恢复设备使用状态"""
        device_id = self.device_id_var.get().strip()
        manufacturer = self.manufacturer_var.get()

        if not device_id:
            messagebox.showwarning("警告", "请输入设备ID")
            return

        def restore():
            log_message(f"开始恢复{manufacturer}设备使用状态: {device_id}")
            try:
                if manufacturer in ["精隆华", "精华隆"]:
                    result = jlh_instance.JHL_devices_huifushiyong(device_id)
                elif manufacturer in ["驰通达", "夜狼"]:
                    result = hm_devices_huifu_status(device_id)
                else:
                    result = f"不支持{manufacturer}设备的恢复操作"

                # 更新设备信息显示
                self.search_device()
                messagebox.showinfo("结果", str(result))
            except Exception as e:
                log_message(f"恢复设备失败: {str(e)}")
                messagebox.showerror("错误", f"恢复设备失败: {str(e)}")

        threading.Thread(target=restore, daemon=True).start()

    def activate_device(self):
        """激活设备"""
        device_id = self.device_id_var.get().strip()
        manufacturer = self.manufacturer_var.get()

        if not device_id:
            messagebox.showwarning("警告", "请输入设备ID")
            return

        def activate():
            log_message(f"开始激活{manufacturer}设备: {device_id}")
            try:
                if manufacturer in ["精隆华", "精华隆"]:
                    result = jlh_instance.device_status_huifu(device_id)
                elif manufacturer in ["驰通达", "夜狼"]:
                    result = hm_devices_jihuo(device_id)
                else:
                    result = f"不支持{manufacturer}设备的激活操作"

                # 更新设备信息显示
                self.search_device()
                messagebox.showinfo("结果", str(result))
            except Exception as e:
                log_message(f"激活设备失败: {str(e)}")
                messagebox.showerror("错误", f"激活设备失败: {str(e)}")

        threading.Thread(target=activate, daemon=True).start()

    def add_device(self):
        """添加设备"""
        device_id = self.device_id_var.get().strip()
        manufacturer = self.manufacturer_var.get()

        if not device_id:
            messagebox.showwarning("警告", "请输入设备ID")
            return

        def add():
            log_message(f"开始添加{manufacturer}设备: {device_id}")
            try:
                if manufacturer in ["精隆华", "精华隆"]:
                    result = jlh_instance.JLH_devices_add(device_id)
                elif manufacturer == "爱奥乐":
                    result = aal_devices_add(device_id)
                elif manufacturer in ["驰通达", "夜狼"]:
                    result = HM_devices_add(device_id)
                else:
                    result = f"不支持{manufacturer}设备的添加操作"

                messagebox.showinfo("结果", str(result))
            except Exception as e:
                log_message(f"添加设备失败: {str(e)}")
                messagebox.showerror("错误", f"添加设备失败: {str(e)}")

        threading.Thread(target=add, daemon=True).start()

    def search_user(self):
        """搜索用户"""
        username = self.username_var.get().strip()

        if not username:
            messagebox.showwarning("警告", "请输入用户名")
            return

        def search():
            log_message(f"开始搜索用户: {username}")
            try:
                result = sousuo_user(username)
                if isinstance(result, dict):
                    self.current_user_id = result.get('用户id')
                    self.user_info_var.set(f"找到用户: {result.get('用户名')} (ID: {result.get('用户id')})")
                else:
                    self.current_user_id = None
                    self.user_info_var.set(str(result))
            except Exception as e:
                log_message(f"搜索用户失败: {str(e)}")
                messagebox.showerror("错误", f"搜索用户失败: {str(e)}")

        threading.Thread(target=search, daemon=True).start()

    def bind_device(self):
        """绑定设备到用户"""
        device_id = self.device_id_var.get().strip()
        manufacturer = self.manufacturer_var.get()

        if not device_id:
            messagebox.showwarning("警告", "请输入设备ID")
            return

        if not self.current_user_id:
            messagebox.showwarning("警告", "请先搜索并选择用户")
            return

        def bind():
            log_message(f"开始绑定设备 {device_id} 到用户 {self.current_user_id}")
            try:
                # 先获取设备信息
                device_info = devices_select(manufacturer, device_id)
                if not device_info or '设备id' not in device_info:
                    messagebox.showerror("错误", "未找到设备信息，无法绑定")
                    return

                # 执行绑定
                result = devicces_bangding(
                    self.current_user_id,
                    device_info.get('设备id'),
                    device_info.get('设备名称', '未知设备')
                )
                messagebox.showinfo("绑定结果", str(result))
            except Exception as e:
                log_message(f"绑定设备失败: {str(e)}")
                messagebox.showerror("错误", f"绑定设备失败: {str(e)}")

        threading.Thread(target=bind, daemon=True).start()

    def run_select_image(self):
        """运行选择图片扫码功能"""
        threading.Thread(target=select_image, daemon=True).start()

    def run_scan_camera(self):
        """运行摄像头扫码功能"""
        threading.Thread(target=scan_from_camera, daemon=True).start()


# 主程序入口
if __name__ == "__main__":
    root = Tk()
    app = DeviceBindingApp(root)
    root.mainloop()
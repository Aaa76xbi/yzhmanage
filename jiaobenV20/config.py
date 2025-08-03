
class JLHconfig:
    login_url = 'https://webapi.nbiotyun.com/login/multipartAccount'  # 登录
    select_changjia_url = 'https://webapi.nbiotyun.com/login/multipartAccountLogin'  # 选择供应商
    shebei_liest_url = 'https://webapi.nbiotyun.com/system/index/menuTree'  # 设备列表
    device_search_url = 'https://webapi.nbiotyun.com/device/deviceList'  # 设备搜索
    huifu_device_status_url = 'https://webapi.nbiotyun.com/deviceState/enable'  # 恢复设备使用状态
    jihuo_device_url = 'https://webapi.nbiotyun.com/deviceState/reset'  # 激活设备
    devices_add_url = 'https://webapi.nbiotyun.com/device/add'


    hm_login_url = 'https://webapi.nbiotyun.com/login/multipartAccountLogin'
    hm_devices_sousuo_url = 'https://webapi.nbiotyun.com/device/deviceList'
    hm_devices_huifushiyong_ul = 'https://webapi.nbiotyun.com/deviceState/enable'
    hm_devices_fuwei_url = 'https://webapi.nbiotyun.com/deviceState/reset'
    hm_add_devices_url = 'https://webapi.nbiotyun.com/device/add'

    def login(self):
        login_dict = {
            "headers": {
                'Cache-Control': 'no-cache', 'User-Agent': 'PostmanRuntime/7.43.4', 'Accept': '*/*'
            },
            "data": {
            'phonenumber': '17286367919',
            'password': 'WDaCw5xqM/FoJhKuC4q3OZ2IVeNd1mjuqcWCZ+UgQ9rbTMinvvzf3slpYNvuBlWs/6FOqsYLoKaCKfp07YLmCmWJkqrH6iJ/XMx2UUAB43tnemmFRszjEreKFiqfHR2VtBLIvr6cRRGcYvADm9jiuuzNBC8EZYyQl29Jjzm3GhE=',
            'clientFlag': '1',
            'phoneCode': '+86',
        }

        }
        return login_dict

    def devices_add(self,device_id):
        devices_add_dict = {
            'headers': {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        },
            'data': {
                  "deviceType": "",
                  "deviceVersionId": "",
                  "deviceBatchId": "",
                  "accessFlag": 1,
                  "deviceImei": device_id,
                  "boxNum": ""
                }
        }

        return devices_add_dict

    def select_gongyingshang(self,changjia_id):

        select_dict = {
            'headers': {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        },
        'data': {
            'phonenumber': '17286367919',
            'password': 'WDaCw5xqM/FoJhKuC4q3OZ2IVeNd1mjuqcWCZ+UgQ9rbTMinvvzf3slpYNvuBlWs/6FOqsYLoKaCKfp07YLmCmWJkqrH6iJ/XMx2UUAB43tnemmFRszjEreKFiqfHR2VtBLIvr6cRRGcYvADm9jiuuzNBC8EZYyQl29Jjzm3GhE=',
            'clientFlag': '1',
            'phoneCode': '+86',
            'deptId': '735868'
        }
        }
        return  select_dict

    def devices_list  (self):
        devicesList_dict = {
            'headers': {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        },

        'data3': {
            'clientFlag': '1'
        }
        }

        return devicesList_dict

    def sousuo_device(self,device_id):
        sousuo_device_dict = {
            'headers': {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        },
        'data': {
            "deviceImei": device_id,
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
    }

        return sousuo_device_dict

    def device_status(self,device_id):
        devices_status_dict = {
        'headers': {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        },
        'data': {
            'deviceImeiList': device_id,
            'stateRemark': '设备恢复使用状态'
        }
        }

        return devices_status_dict

    def devices_jihuo(self,device_id):

        devices_jihuo_dict = {
            'headers': {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        },
        'data': {
            'deviceImeiList': device_id
        }
        }

        return devices_jihuo_dict


class hmConfig:

    def login(self,shangjia_id):
        login_data_dict ={
           'headers': {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        },
            'data': {
                'phonenumber': '17286367919',
                'password': 'WDaCw5xqM/FoJhKuC4q3OZ2IVeNd1mjuqcWCZ+UgQ9rbTMinvvzf3slpYNvuBlWs/6FOqsYLoKaCKfp07YLmCmWJkqrH6iJ/XMx2UUAB43tnemmFRszjEreKFiqfHR2VtBLIvr6cRRGcYvADm9jiuuzNBC8EZYyQl29Jjzm3GhE=',
                'clientFlag': '1',
                'phoneCode': '+86',
                'deptId': shangjia_id
            }
        }

        return login_data_dict

    def deviuces_sosuo(self,devices_id):

        devices_sosuo_dict = {
            'data': {
                  "deviceImei": devices_id,
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
                },
            'headers': {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        }

        }

        return devices_sosuo_dict

    def hm_devices_add(self,devices_id):
        hm_devices_add_dict = {
            'data': {
              "deviceType": "",
              "deviceVersionId": "",
              "deviceBatchId": "",
              "accessFlag": 1,
              "deviceImei": devices_id,
              "boxNum": ""
            },
            'headers': {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        }

        }
        return  hm_devices_add_dict

    def  hm_devices_jihuo(self,devices_id):
        hm_devices_jihuo_dict = {
            'data': {
              "deviceImeiList": devices_id
            },
            'headers': {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        }

        }
        return  hm_devices_jihuo_dict

    def  hm_devices_huifu(self,devices_id):
        hm_devices_huifu_dict = {
            'data': {
              "deviceImeiList": devices_id,
              "stateRemark": "设备恢复使用状态"
            },
            'headers': {
            'Cache-Control': 'no-cache',
            'User-Agent': 'PostmanRuntime/7.43.4',
            'Accept': '*/*',
        }

        }
        return  hm_devices_huifu_dict


class YZHconfig:
    yzh_login_url = 'https://admin.11yzh.com/admin/login/index.html'#登录
    JHL_devicesList_url = 'https://admin.11yzh.com/admin/deviceinnopronew/finder?page=1&limit=20'#精隆华设备列表
    JHL_devices_tongbu_url = 'https://admin.11yzh.com/admin/deviceinnopronew/_synupdate'  #精隆华设备同步
    JHL_devices_sousuo_url = 'https://admin.11yzh.com/admin/deviceinnopronew/finder?page=1&limit=20&name=860722078836069&use_id=&type_id=&status='#设备搜索
    YHZusers_sousuo_url = 'https://admin.11yzh.com/admin/cuserarchives/finder'#用户搜索
    JHl_devices_bangdingUESR_url = 'https://admin.11yzh.com/admin/devicecuser/create'#设备绑定用户
    daping_username_url = 'https://admin.11yzh.com/admin/datalogin/finder'#大屏账号列表
    yzh_HMdevices_tongbu_url = 'https://admin.11yzh.com/admin/devicectdyun/_synupdate'#hm设备数据同步
    yzh_aal_devices_add_url = 'https://admin.11yzh.com/admin/devicegprss/create'#爱奥乐设备添加yzh平台


    def login_data(self):
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
        lodin_data = {
            'data': data,
            'headers': headers
        }
        return  lodin_data

    def yzh_user_sousuo(self,username):
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            # "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
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
        sousuo_user_data = {
            'data': data,
            'headers': headers
        }
        return sousuo_user_data

    def yzh_hmdevices_sousuo(self,devices_id):

        headers = {
      "accept": "application/json, text/javascript, */*; q=0.01",
      "accept-encoding": "gzip, deflate, br, zstd",
      "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
      # "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
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
        return  headers

    def yzh_hmdevices_tongbu_mydql(self):
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-length": "0",
            # "cookie": "PHPSESSID=ca1eb5132e4e64fda77036854a7d2a63",
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
        return  headers
    def yzh_JLHdeives_tongbu(self):
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            # "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
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
        return headers
    def yzh_devices_sousuo(self,deivice_id):
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            # "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
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
            "name": deivice_id,
            "use_id": "",
            "type_id": "",
            "status": ""
        }
        yzh_devices_sousuo = {
            'data': data,
            'headers': headers
        }
        return  yzh_devices_sousuo
    def yzh_aal_devices_add(self,device_id,device_name):
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
        yzh_aal_devices_add = {
            'data': data,
            'headers': headers
        }
        return yzh_aal_devices_add

    def aal_devices_sousuo(self):
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            # "cookie": "PHPSESSID=ca1eb5132e4e64fda77036854a7d2a63",
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
        return  headers

    def yzh_devices_bangding(self,user_id,device_id,type_name):
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-length": "294",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "cookie": "PHPSESSID=a92a1888cf6aa9bb50a60006e270779f",
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
        yzh_devices_bangding = {
            'data': data,
            'headers': headers
        }
        return yzh_devices_bangding



class AAl_config:
    aal_add_devices_url = 'http://tf.ydjk5.com/gprs/dev/rule/add'
    aal_devices_sousuo_url = 'http://tf.ydjk5.com/gprs/dev/rule/list'

    def aal_login(self):
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

        return headers

    def aal_adddevices(self,device_id):
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

        xuetangyi_data = {
            "brandId": "f843e5c8-34a6-4a9d-9ff3-1b7c160a8acb",
            "deptId": "0f28de53-7506-46f8-868e-8f3a504a0ee1",
            "devicesModel": "1",
            "devicesSn": f"{device_id}###",
            "devicesType": "2",
            "transmitlFlag": "1",
            "userOneTransmitlFlag": "1",
            "userTwoTransmitlFlag": "1"
        }
        aal_adddevices_data = {
            'data': data,
            'headers': headers,
            'xuetangyi_data': xuetangyi_data
        }
        return  aal_adddevices_data

    def aal_devices_sousuo(self,device_id):
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
        data = {'brandName': "", 'deptName': "", 'devSN': device_id, 'page': 1, 'rows': 10}
        aal_devices_sousuo_data = {
            'data': data,
            'headers': headers
        }
        return aal_devices_sousuo_data
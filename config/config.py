
class JLHconfig:
    login_url = 'https://webapi.nbiotyun.com/login/multipartAccount'  # 登录
    select_changjia_url = 'https://webapi.nbiotyun.com/login/multipartAccountLogin'  # 选择供应商
    shebei_liest_url = 'https://webapi.nbiotyun.com/system/index/menuTree'  # 设备列表
    device_search_url = 'https://webapi.nbiotyun.com/device/deviceList'  # 设备搜索
    huifu_device_status_url = 'https://webapi.nbiotyun.com/deviceState/enable'  # 恢复设备使用状态
    jihuo_device_url = 'https://webapi.nbiotyun.com/deviceState/reset'  # 激活设备

    hm_login_url = 'https://webapi.nbiotyun.com/login/multipartAccountLogin'
    hm_devices_sousuo_url = 'https://webapi.nbiotyun.com/device/deviceList'

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
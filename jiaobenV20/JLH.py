import requests
from  jiaobenV20.config import JLHconfig,hmConfig

request_data = JLHconfig()
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
        if  select_response.json().get('msg') == '操作成功':
            print('JLH登陆成功！', select_response.json())

    def JLH_devices_sousuo(self, devices_id):  ### 精隆华设备搜索
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
            return {"错误": "未找到设备数据"}

        row_data = rows[0]
        device_data = {
            '使用状态': row_data.get('usingStatusName'),
            '激活状态': row_data.get('stateName'),
            '设备厂商': row_data.get('deviceMakerName'),
            '设备名称': row_data.get('deviceTypeName'),
            '设备编号': devices_id
        }
        return device_data

    def JHL_devices_huifushiyong(self,device_id):#精隆华设别恢复使用状态


        data = request_data.device_status(device_id).get('data')
        headers = request_data.device_status(device_id).get('headers')
        huifu_device_status = self.session.post(JLHconfig.huifu_device_status_url, data=data, headers=headers,
                                           proxies=JLH_caozuo.proxies)  # 设备恢复使用状态
        if  huifu_device_status.json().get('msg') == '操作成功':
            print('设备回复使用状态成功！', huifu_device_status)
            return {'使用状态': '正常使用'}


    def device_status_huifu(self,device_id):#精隆化设备复位状态
            data = request_data.devices_jihuo(device_id).get('data')
            headers = request_data.devices_jihuo(device_id).get('headers')
            jihuo_device = self.session.post(JLHconfig.jihuo_device_url, data=data, headers=headers,
                                        proxies=JLH_caozuo.proxies)  # 复位设别的状态为：正常
            print('设备激活成功！', jihuo_device.json())
            return {'激活状态': '正常'}

    def JLH_devices_add(self,device_id):
        data = request_data.devices_add(device_id).get('data')
        headers = request_data.devices_add(device_id).get('headers')
        devices_add = self.session.post(JLHconfig.devices_add_url,  data=data, headers=headers,)
        add_xinxi = devices_add.json()
        print(add_xinxi)
        return add_xinxi




jlh_instance = JLH_caozuo()
# result = jlh_instance.JLH_devices_sousuo('866940073226722')
# huifu  =  jlh_instance.JHL_devices_huifushiyong('860722078836069')
# huifuzhuangtai = jlh_instance.device_status_huifu('860722078836069')
# devices_add = jlh_instance.JLH_devices_add('868366078240088')
# print(result)
# print(huifu)
# print(huifuzhuangtai)
# print(devices_add)


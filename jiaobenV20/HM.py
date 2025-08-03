from jiaobenV20.config import *
import  requests


# hm_devices_tongbu_msql()
class HM_caozuo:
    proxies = {
        'http': None,
        'https': None
    }
    session = requests.Session()
    def __init__(self):
        data = hmConfig().login('636250').get('data')
        headers = hmConfig().login('636250').get('headers')

        select_response = self.session.post(JLHconfig.select_changjia_url, data=data, headers=headers, proxies=self.proxies)  # 选择供应商
        print('HM平台',select_response.json())

    def HM_devices_select(self,devices_id):

        date = hmConfig().deviuces_sosuo(devices_id).get('data')
        headers = hmConfig().deviuces_sosuo(devices_id).get('headers')
        response = self.session.post(JLHconfig().hm_devices_sousuo_url, data=date, headers=headers, proxies=self.proxies)
        print(response.json().get('rows'))
        devices = response.json().get('rows')
        if  len(devices) == 0:
            print('设备未找到！请检查设备编号号是否正确！')
            device_data = {
                '设备厂商': '',
                '设备名称': '',
                '设备编号': '',
                '设备状态': '',
                '设备使用状态': '',
            }
            return device_data
        else:
            print('设备已找到！', devices)
            device_data = {
                '设备厂商': devices[0].get('deviceMakerName'),
                '设备名称': devices[0].get('deviceTypeName'),
                '设备编号': devices[0].get('deviceImei'),
                '设备状态': devices[0].get('stateName'),
                '设备使用状态': devices[0].get('usingStatusName'),
            }
            return device_data



    def  hm_devices_huifu_shiyong(self,device_id):
        # 禁用代理（根据之前的错误信息）


        data = hmConfig().login('636250').get('data')
        headers = hmConfig().login('636250').get('headers')


        select_response = self.session.post(JLHconfig.select_changjia_url, data=data, headers=headers, proxies=self.proxies)  # 选择供应商

        date = hmConfig().hm_devices_huifu(device_id).get('data')
        headers = hmConfig().hm_devices_huifu(device_id).get('headers')
        response = self.session.post(JLHconfig().hm_devices_huifushiyong_ul, data=date, headers=headers, proxies=self.proxies)
        print('hm设备恢复',response.json())
        return response.json()



    def HM_devices_add(self,device_id):

        data = hmConfig().login('636250').get('data')
        headers = hmConfig().login('636250').get('headers')

        select_response = self.session.post(JLHconfig.select_changjia_url, data=data, headers=headers, proxies=self.proxies)  # 选择供应商
        data = hmConfig().hm_devices_add(device_id).get('data')
        headers = hmConfig().hm_devices_add(device_id).get('headers')
        add_device = self.session.post(JLHconfig().hm_add_devices_url,headers=headers,data=data,proxies=self.proxies)
        add_device_xinxi = add_device.json()
        print(add_device_xinxi)
        return  add_device_xinxi


    def  hm_devices_jihuo(self,device_id):
        jihuo_url = 'https://webapi.nbiotyun.com/deviceState/reset'
        data = hmConfig().login('636250').get('data')
        headers = hmConfig().login('636250').get('headers')


        select_response = self.session.post(JLHconfig.select_changjia_url, data=data, headers=headers, proxies=self.proxies)  # 选择供应商
        data = hmConfig().hm_devices_jihuo(device_id).get('data')
        headers = hmConfig().hm_devices_jihuo(device_id).get('headers')
        jihuo_device = self.session.post(JLHconfig().hm_devices_fuwei_url,headers=headers,data=data,proxies=self.proxies)
        fuwei_jieguo =  jihuo_device.json()
        print('复位（激活）设备',fuwei_jieguo)
        return fuwei_jieguo




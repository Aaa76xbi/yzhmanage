import  requests
from jiaobenV20.config import AAl_config

class  AAL_caozuo:
    proxies = {'http': None, 'https': None}
    aal_sesson = requests.session()

    def __init__(self):
        aal_login_url = 'http://tf.ydjk5.com/gprs/login'  # 确认URL正确性
        data = {'username': "gzyzh", 'password': "gz123456"}
        login = self.aal_sesson.post(
            aal_login_url,
            json=data,  # 替换data=data为json=data
            headers=AAl_config().aal_login(),
            proxies=self.proxies
        )
        print('爱奥乐平台',login.json())

    def aal_devices_add(self,device_id):
        add_devices = self.aal_sesson.post(
            AAl_config().aal_add_devices_url,headers=AAl_config().aal_adddevices(device_id).get('headers'),
            json=AAl_config().aal_adddevices(device_id).get('data'),
        )
        print(add_devices.json())
        return add_devices.json()

    def aal_devices_sousuo(self,device_id):

        device_sousuo = self.aal_sesson.post(
            AAl_config().aal_devices_sousuo_url,
            headers=AAl_config().aal_devices_sousuo(device_id).get('headers'),
            json=AAl_config().aal_devices_sousuo(device_id).get('data')
        )
        data = device_sousuo.json().get('data').get('list')
        if data != []:
            device_name = device_sousuo.json().get('data').get('list')[0].get('devicesTypeNum')
            device_id = device_sousuo.json().get('data').get('list')[0].get('devicesSn')
            # print(device_sousuo.json().get('data').get('list')[0])
            devices_data = {
                '设备名称': f'{device_name}仪',
                '设备id':device_id,
                '设备厂商':'爱奥乐'
            }
            return devices_data
        else:
            print('未找到设备',device_sousuo.json())

aal = AAL_caozuo()
# aal.aal_devices_add('25C005777')
print(aal.aal_devices_sousuo(device_id='25C006209'))
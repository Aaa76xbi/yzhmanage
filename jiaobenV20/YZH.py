import requests
from pywin.scintilla.document import re_encoding_text

from jiaobenV20.config import YZHconfig, JLHconfig
import time

#益智慧平台
cishu = 0
class YZH_caozuo:
    yzh_session = requests.session()
    proxies = {
        'http': None,
        'https': None
    }

    #查询大屏账号是否存在
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

    # response = yzh_session.get(daping_username_url, headers=headers, proxies=proxies)
    # print('大屏账号列表',response.json().get('data'))
    # daping_list =  response.json().get('data')
    # for i in daping_list:
    #     print(i)


    def __init__(self):

        response = self.yzh_session.post(YZHconfig.yzh_login_url, data=YZHconfig().login_data().get('data'), headers=YZHconfig().login_data().get('headers'), proxies=self.proxies)#登录益智慧平台
        print('益智慧平台登录结果：',response.json())
    #查询用户是否存在
    def sousuo_user(self,username):

        response = self.yzh_session.post(
            YZHconfig.YHZusers_sousuo_url,
            data=YZHconfig().yzh_user_sousuo(username).get('data'),
            headers=YZHconfig().yzh_user_sousuo(username).get('headers'),
            proxies=self.proxies
        )#用户搜索
        user_list = response.json().get('data')

        if len(user_list) != 0:
            print('用户列表是：', user_list)
            print(user_list[0].get('id'))
            user_id = user_list[0].get('id')
            user_data = {
                '用户名': user_list[0].get('name'),
                '用户id': user_id,
            }
            print('已找到用户')
            return user_data
        else:
            return 0


    # print(sousuo_user(username='赵德柱'))
    def hm_devices_sousuo(self,devices_id):
        devices_id = str(devices_id)
        hm_devices_url = f'https://admin.11yzh.com/admin/devicectdyun/finder?page=1&limit=20&name={devices_id}&use_id=&type_id=&status='


        devices_sousuo = self.yzh_session.get(
            hm_devices_url, headers=YZHconfig().yzh_hmdevices_sousuo(devices_id)
        )
        devices_sousuo_jieguo = devices_sousuo.json()
        print('搜索设备结果：',devices_sousuo_jieguo)
        return devices_sousuo_jieguo

    def yzh_HMdevices_tongbu_msql(self):
        tongbu = self.yzh_session.post(YZHconfig().yzh_HMdevices_tongbu_url, headers=YZHconfig().yzh_hmdevices_tongbu_mydql(), proxies=self.proxies)
        tongbu_jieguuuo = tongbu.json()
        print(tongbu_jieguuuo)
        return tongbu_jieguuuo

    def yzh_JLHdevices_tongbu_mysql(self):
        print('正在同步数据库......')
        response = self.yzh_session.post(
            YZHconfig().JHL_devices_tongbu_url,
            headers=YZHconfig().yzh_JLHdeives_tongbu().get('headers'),
            proxies=self.proxies
        )
        # print(response.json().get('msg'))
        tongbu_xinxi = response.json().get('msg')
        if tongbu_xinxi == '同步成功！':
            print('同步成功！')
            return response.json()
        else:
            print('同步失败！')
            return response.json()


    def yzh_JLHdevicees_sousuo(self,device_id):
        url = f'https://admin.11yzh.com/admin/devicectdyun/finder?page=1&limit=20&name={device_id}&use_id=&type_id=&status='
        response = self.yzh_session.get(
            url,
            # data=YZHconfig().yzh_devices_sousuo(device_id).get('data'),
            headers=YZHconfig().yzh_devices_sousuo(device_id).get('headers'),
            proxies=self.proxies
        )
        print(response.json())
        if len(response.json().get('data')) != 0:
            device_id = response.json().get('data')[0].get('device_id')
            type_name = response.json().get('data')[0].get('type_name')
            # print('设备id',response.json().get('data')[0].get('type_name'))
            device_data = {
                '设备名称': type_name,
                '设备id': device_id,
            }
            print('设备存在！信息为：', type_name, device_id)
            return device_data
        else:
            print('设备不存在列表！正在同步数据库......')
            YZH_caozuo().yzh_JLHdevices_tongbu_mysql()
            time.sleep(1.2)
            print('请继续继续查询结果！')

    def aal_devices_YZHadd(self,device_name, device_id):
        """爱奥乐设备添加yzh平台"""
        device_add = self.yzh_session.post(
            YZHconfig().yzh_aal_devices_add_url,
            headers=YZHconfig().yzh_aal_devices_add(device_name, device_id).get('headers'),
            data=YZHconfig().yzh_aal_devices_add(device_name, device_id).get('data'),
        )
        print(device_add.json())
        return device_add.json()

    def aal_device_YZHshousuo(self,device_id):
        """爱奥乐设备搜索yzh平台"""
        url = f'https://admin.11yzh.com/admin/devicegprss/finder?page=1&limit=20&name={device_id}&use_id=&type_id=&zone_id=0&code=&province_code=&city_code=&area_code=&street_code=&village_code=&level=1'
        try:
            # 添加超时参数（如10秒），避免无限等待
            sousuo = self.yzh_session.get(
                url,
                headers=YZHconfig().aal_devices_sousuo(),
                timeout=10
            )
            data = sousuo.json().get('data')
            if  len(data) == 0:
                print('设备没有找到哦,返回数据：',sousuo.json())
                return  '设备没有找到哦'
            else:
                device_id = sousuo.json().get('data')[0].get('device_id')
                print('找到设备aal-yzh设备搜索id：', sousuo.json().get('data')[0].get('device_id'))
                return device_id
        except Exception as e:
            print('请求出错：', str(e))  # 捕获超时、解析错误等异常

    def devicces_bangding(self,user_id, device_id, type_name):
        """设备绑定yzh平台"""
        response = self.yzh_session.post(
            YZHconfig().JHl_devices_bangdingUESR_url,
            data=YZHconfig().yzh_devices_bangding(user_id, device_id, type_name).get('data'),
            headers=YZHconfig().yzh_devices_bangding(user_id, device_id, type_name).get('headers'),
            proxies=self.proxies
        )
        print(response.json(), '456' * 100)
        msg = response.json().get('msg')
        print(msg)
        if msg == '一个用户不能重复绑定相同的设备！':
            print('该设备已绑定！---->', response.json())
            return msg
        else:
            print('绑定成功！---->', response.json())
            return msg


# yzh = YZH_caozuo()
# print(yzh.sousuo_user(username='赵德柱'))
# print(yzh.hm_devices_sousuo(866940073226722))
# yzh.yzh_HMdevices_tongbu_msql()
# print(yzh.yzh_JLHdevicees_sousuo(device_id='860376061283217'))
# yzh.yzh_JLHdevices_tongbu_mysql()
# yzh.aal_devices_YZHadd(device_name='血压仪', device_id='25B024275')
# print(yzh.aal_device_YZHshousuo('25B020789'))
# yzh.devicces_bangding(user_id=532, device_id='502', type_name='烟感报警器')
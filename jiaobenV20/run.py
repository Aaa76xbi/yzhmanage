from jiaobenV20.config import JLHconfig,hmConfig
hm_config = hmConfig()
from jiaobenV20.YZH import YZH_caozuo
from jiaobenV20.JLH import JLH_caozuo
from jiaobenV20.AAL import AAL_caozuo
from jiaobenV20.HM import HM_caozuo
import XiangJiFangFa
print('正在打开 益智慧设备绑定程序.......')


choose = '2'
continue_exec = True  # 控制标志位

if choose == '1':
    print('请等待一下，这个功能一会开发')
elif choose == '2':
    print('正在加载摄像头......')
    device_data = XiangJiFangFa.scan_from_camera()
    print(device_data)
    print('设备信息：',
          device_data.get('设备名称'),
          device_data.get('设备编号'),
          device_data.get('设备厂商')
          )

    if device_data.get('设备厂商') in ['精隆华', '精华隆']:
        print('正在初始化设备......')
        if device_data.get('使用状态') == '正常使用':
            jlh = JLH_caozuo()
            jieguo = jlh.JHL_devices_huifushiyong(device_data.get('设备编号'))
            print('场景1-正在恢复使用状态.....', jieguo)
            jieguo = jlh.device_status_huifu(device_data.get('设备编号'))
            print('场景1-正在复位设备状态.....', jieguo)

            user_name = input('设备初始化完成，请输入绑定用户姓名：')
            zhi = YZH_caozuo().sousuo_user(user_name)

            if zhi == 0:
                print(f"没有用户：{user_name}，请为其添加健康档案！")
                continue_exec = False  # 标记为不继续执行

            # 关键：用标志位判断，只有continue_exec为True时才执行后续代码
            if continue_exec:
                print('正在绑定用户......')
                yonghusousuo = YZH_caozuo().sousuo_user(user_name)
                print('第二步是否执行')
                print(device_data.get('设备编号'), device_data.get('设备厂商'), '&' * 100)
                device_data = YZH_caozuo().yzh_JLHdevicees_sousuo(device_data.get('设备编号'))
                # print(yonghusousuo.get('用户id'), device_data.get('设备id'), device_data.get('设备名称'))
                YZH_caozuo().devicces_bangding(yonghusousuo.get('用户id'), device_data.get('设备id'), device_data.get('设备名称'))
                print('绑定成功！')


    elif device_data.get('设备厂商') in ['夜狼','驰通达']:
        print(f'正在初始化{device_data.get("设备厂商")}设备......')
        jlh = HM_caozuo()
        jieguo = jlh.hm_devices_huifu_shiyong(device_data.get('设备编号'))
        print('场景2-正在恢复使用状态.....', jieguo)
        jieguo = jlh.hm_devices_jihuo(device_data.get('设备编号'))
        print('场景2-正在复位设备状态.....', jieguo)

        user_name = input('设备初始化完成，请输入绑定用户姓名：')
        zhi = YZH_caozuo().sousuo_user(user_name)

        if zhi == 0:
            print(f"没有用户：{user_name}，请为其添加健康档案！")
            continue_exec = False  # 标记为不继续执行

        # 关键：用标志位判断，只有continue_exec为True时才执行后续代码
        if continue_exec:
            print('正在绑定用户......')
            print(device_data.get('设备编号'), device_data.get('设备厂商'), '&' * 100)
            device_data = YZH_caozuo().yzh_JLHdevicees_sousuo(device_data.get('设备编号'))
            # print(yonghusousuo.get('用户id'), device_data.get('设备id'), device_data.get('设备名称'))
            YZH_caozuo().devicces_bangding(zhi.get('用户id'),
                                           device_data.get('设备id'),
                                           device_data.get('设备名称')
                                           )
            print('绑定成功！')

#
    else:
        print(f'正在初始化{device_data.get("设备厂商")}设备......')
        aal = AAL_caozuo()
        aal.aal_devices_sousuo(device_data.get('设备编号'))
        aal.aal_devices_add(device_data.get('设备编号'))

        user_name = input('设备初始化完成，请输入绑定用户姓名：')
        zhi = YZH_caozuo().sousuo_user(user_name)

        if zhi == 0:
            print(f"没有用户：{user_name}，请为其添加健康档案！")
            continue_exec = False  # 标记为不继续执行

        # 关键：用标志位判断，只有continue_exec为True时才执行后续代码
        if continue_exec:
            print('正在绑定用户......')
            print(device_data.get('设备id'), device_data.get('设备厂商'), '&' * 100)
            device_data002 = YZH_caozuo().aal_device_YZHshousuo(device_data.get('设备id'))
            print(zhi.get('用户id'), device_data.get('设备id'), device_data.get('设备名称'))
            YZH_caozuo().devicces_bangding(zhi.get('用户id'),
                                           device_data002,
                                           device_data.get('设备名称')
                                           )
            print('绑定成功！')
# #===================================================================================================







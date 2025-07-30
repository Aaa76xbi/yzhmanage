import cv2
from tkinter import filedialog, Tk
import numpy as np
from config.config import *
import pyttsx3
import requests

import tkinter as tk
from test_debug.gui import DeviceBindGUI  # 导入上面的界面类

def api_reuqest(device_id):
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

    # response = session.post(login_url, data=data, headers=headers, proxies=proxies) #登录请求
    # print(response.json())

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
    # print(select_response.json())

    headers = {
        'Cache-Control': 'no-cache',
        'User-Agent': 'PostmanRuntime/7.43.4',
        'Accept': '*/*',
    }
    data4 = {
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
    device_search = session.post(device_search_url, data=data4, headers=headers, proxies=proxies)#设备搜索
    print(device_search.json())
    stateName = device_search.json().get('rows')[0].get('stateName')# 激活状态
    usingStatusName = device_search.json().get('rows')[0].get('usingStatusName')#使用状态
    deviceTypeName = device_search.json().get('rows')[0].get('deviceTypeName')#设备类型名称
    deviceMakerName = device_search.json().get('rows')[0].get('deviceMakerName')#设备厂商
    # print(stateName, usingStatusName, deviceTypeName, deviceMakerName)

    device_data = {
        '使用状态': usingStatusName,
        '激活状态':stateName,
        '设备厂商': deviceMakerName,
        '设备名称': deviceTypeName,
        '设备编号': device_id
    }
    return device_data


print(api_reuqest(860722078836069))


def simple_speak(text):
    engine = pyttsx3.init()  # 初始化
    engine.say(text)  # 加入朗读内容
    engine.runAndWait()  # 执行朗读

# simple_speak("烟感检测报警器已识别！是否需要绑定？设备编号：2132535hyGG2")




# 初始化 FreeType 字体渲染器
# ft = cv2.freetype.createFreeType2()
# # 替换为系统中真实存在的中文字体路径，如 Windows 下的“msyh.ttc”
# ft.loadFontData(fontFileName=r'D:\pythonProject_mannageYZH\shebei_auto\simhei.ttf', id=0)


def decode_qrcode_from_image(image_path):
    """从图像路径读取并解码二维码的函数"""
    image = cv2.imread(image_path)
    result, _ = detect_and_decode_strict(image)
    return result


def select_image():
    """打开文件选择对话框选择图像的函数"""
    Tk().withdraw()
    file_path = filedialog.askopenfilename(title="快来选择你的图片吧~~🚀",
                                           filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        image = cv2.imread(file_path)
        data, bbox = detect_and_decode_strict(image)
        if data:
            print(f"[图片识别成功] 已解码: {data}")
            cv2.putText(image, f"{data}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            # 绘制二维码边框（增加安全检查）
            if bbox is not None and len(bbox) >= 4:
                for i in range(4):
                    cv2.line(image, tuple(bbox[i]), tuple(bbox[(i + 1) % 4]), (255, 0, 0), 2)

            cv2.imshow("识别结果", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("图片好像有点小问题，没有识别到哎~~~")


def enhance_image(image):
    """增强图像质量以便更好地检测二维码的函数"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharp = cv2.filter2D(gray, -1, sharpen_kernel)
    return sharp


def detect_and_decode_strict(image):
    """严格检测和解码二维码的函数（尝试多种方法提高成功率）"""
    detector = cv2.QRCodeDetector()
    gray = enhance_image(image)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # 确保ROI区域足够大，避免过小的无效区域
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
            print(f"处理ROI时出错: {e}")
            continue  # 继续尝试其他轮廓

    return None, None  # 未检测到二维码


def scan_from_camera():
    cap = cv2.VideoCapture(0)
    print("🚀 启动摄像头扫码（识别到二维码后自动停止）")
    result = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法获取摄像头画面，退出...")
            break

        data, bbox = detect_and_decode_strict(frame)
        if data:
            result = data
            print(f"[✅ 识别成功] 二维码内容: {data}")
            device_data = api_reuqest(data)  # 获取设备信息

            # 生成语音文本
            yuyin_txt = f"{device_data.get('设备名称')}已识别！是否需要绑定？设备编号：{device_data.get('设备编号')}"

            # 关键修改：通过界面实例调用语音和弹窗
            app.speak_text(yuyin_txt)  # 播报语音
            app.show_device_dialog(device_data)  # 显示弹窗

            # 绘制边框并显示1秒
            cv2.putText(frame, f"{data}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            if bbox is not None and len(bbox) >= 4:
                for i in range(4):
                    cv2.line(frame, tuple(bbox[i]), tuple(bbox[(i + 1) % 4]), (255, 0, 0), 2)
            cv2.imshow("摄像头扫码", frame)
            cv2.waitKey(1000)
            break
        else:
            # 未识别到二维码时的提示（用英文避免乱码）
            h, w = frame.shape[:2]
            warning_text = "Please hold QR code close to camera"
            cv2.putText(frame, warning_text, (int(w * 0.05), int(h * 0.95)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                        2)
            cv2.imshow("摄像头扫码", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return result


# if __name__ == "__main__":
#     print("选择功能：\n1 - 摄像头识别二维码\n2 - 上传图片识别二维码")
#     choice = input("请输入选项 (1 或 2): ").strip()
#
#     if choice == '1':
#         scan_from_camera()
#     elif choice == '2':
#         select_image()
#     else:
#         print("无效选项，请输入 1 或 2")

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    # 实例化界面，传入你的单设备绑定函数（scan_from_camera）
    global app  # 全局变量，让scan_from_camera能调用界面方法
    app = DeviceBindGUI(root, scan_from_camera)
    # 启动界面
    root.mainloop()
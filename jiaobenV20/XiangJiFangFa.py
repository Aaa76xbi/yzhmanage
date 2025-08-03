import time
import cv2
from tkinter import filedialog, Tk
import numpy as np
import pyttsx3

from jiaobenV20.YZH import  YZH_caozuo
from jiaobenV20.JLH import  JLH_caozuo
from jiaobenV20.HM import HM_caozuo
from jiaobenV20.AAL import  AAL_caozuo

def simple_speak(text):
    engine = pyttsx3.init()  # 初始化
    engine.say(text)  # 加入朗读内容
    engine.runAndWait()  # 执行朗读

# simple_speak("烟感检测报警器已识别！是否需要绑定？设备编号：2132535hyGG2")



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
            # 释放资源后再退出
            cap.release()
            cv2.destroyAllWindows()
            break

        data, bbox = detect_and_decode_strict(frame)
        if data:
            result = data
            print(f"[✅ 识别成功] 二维码内容: {data}")
            device_data = JLH_caozuo().JLH_devices_sousuo(data)  # 获取设备信息
            # print(device_data.get('设备厂商'),'yi'*100)
            if device_data.get('设备厂商') is not None:
                if device_data.get('设备厂商') == '精华隆' or  device_data.get('设备厂商') == '精隆华':
                    # 生成语音文本
                    yuyin2_txt = f"厂商{device_data.get('设备厂商')},设备{device_data.get('设备名称')},使用状态{device_data.get('使用状态')},设备状态{device_data.get('激活状态')}，设备编号{device_data.get('设备编号')}"
                    simple_speak(yuyin2_txt)

                    # 绘制边框并显示1秒
                    cv2.putText(frame, f"{data}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                    if bbox is not None and len(bbox) >= 4:
                        for i in range(4):
                            cv2.line(frame, tuple(bbox[i]), tuple(bbox[(i + 1) % 4]), (255, 0, 0), 2)
                    cv2.imshow("摄像头扫码", frame)
                    cv2.waitKey(1000)

                    # 关键修复：释放摄像头和关闭窗口
                    cap.release()
                    cv2.destroyAllWindows()
                    return device_data
                else:
                    device_data = HM_caozuo().HM_devices_select(data)
                    # print(device_data,'er'*100)
                    if device_data.get('设备厂商') is not None:
                        # 生成语音文本
                        yuyin2_txt = f"厂商{device_data.get('设备厂商')},设备{device_data.get('设备名称')},使用状态{device_data.get('设备状态')},设备状态{device_data.get('设备使用状态')}，设备编号{device_data.get('设备编号')}"
                        simple_speak(yuyin2_txt)

                        # 绘制边框并显示1秒
                        cv2.putText(frame, f"{data}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                        if bbox is not None and len(bbox) >= 4:
                            for i in range(4):
                                cv2.line(frame, tuple(bbox[i]), tuple(bbox[(i + 1) % 4]), (255, 0, 0), 2)
                        cv2.imshow("摄像头扫码", frame)
                        cv2.waitKey(1000)

                        # 关键修复：释放摄像头和关闭窗口
                        cap.release()
                        cv2.destroyAllWindows()
                        return device_data

            JLH_caozuo().JLH_devices_add(data)
            time.sleep(2)
            device_data = JLH_caozuo().JLH_devices_sousuo(data)
            if device_data.get('设备厂商') is not None:
                # print('添加成功')
                scan_from_camera()
                # return device_data
            HM_caozuo().HM_devices_add(data)
            time.sleep(2)
            device_data = HM_caozuo().HM_devices_select(data)
            if device_data.get('设备厂商') in ['夜狼','驰通达']:
                # print('设备添加成功')
                device_data = HM_caozuo().HM_devices_select(data)
                # print(device_data, 'hm' * 100)
                if device_data.get('设备厂商') is not None:
                    # 生成语音文本
                    yuyin2_txt = f"厂商{device_data.get('设备厂商')},设备{device_data.get('设备名称')},使用状态{device_data.get('设备状态')},设备状态{device_data.get('设备使用状态')}，设备编号{device_data.get('设备编号')}"
                    simple_speak(yuyin2_txt)

                    # 绘制边框并显示1秒
                    cv2.putText(frame, f"{data}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                    if bbox is not None and len(bbox) >= 4:
                        for i in range(4):
                            cv2.line(frame, tuple(bbox[i]), tuple(bbox[(i + 1) % 4]), (255, 0, 0), 2)
                    cv2.imshow("摄像头扫码", frame)
                    cv2.waitKey(1000)

                    # 关键修复：释放摄像头和关闭窗口
                    cap.release()
                    cv2.destroyAllWindows()
                    return device_data
            else:
                print(AAL_caozuo().aal_devices_add(data))
                time.sleep(1.5)
                device_data = AAL_caozuo().aal_devices_sousuo(data)  # 获取设备信息
                print(device_data.get('设备厂商'), 'aal' * 100)
                if device_data.get('设备厂商') is not None:

                        # 生成语音文本
                    yuyin2_txt = (f"厂商{device_data.get('设备厂商')},"
                                  f"设备{device_data.get('设备名称')},"
                                  f"设备id{device_data.get('设备id')}"
                                  )
                    simple_speak(yuyin2_txt)

                    # 绘制边框并显示1秒
                    cv2.putText(frame, f"{data}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                    if bbox is not None and len(bbox) >= 4:
                        for i in range(4):
                            cv2.line(frame, tuple(bbox[i]), tuple(bbox[(i + 1) % 4]), (255, 0, 0), 2)
                    cv2.imshow("摄像头扫码", frame)
                    cv2.waitKey(1000)

                    # 关键修复：释放摄像头和关闭窗口
                    cap.release()
                    cv2.destroyAllWindows()
                    return device_data


        else:
            # 未识别到二维码时的提示（用英文避免乱码）
            h, w = frame.shape[:2]
            warning_text = "Please hold the QR code close to the camera --- Aaa76MaBy"
            cv2.putText(frame, warning_text, (int(w * 0.05), int(h * 0.95)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                        2)
            cv2.imshow("摄像头扫码", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return result


# print(scan_from_camera())
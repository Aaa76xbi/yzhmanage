# import cv2
# from tkinter import filedialog, Tk
# import numpy as np
#
#
# def decode_qrcode_from_image(image_path):
#     image = cv2.imread(image_path)
#     result = detect_and_decode_strict(image)
#     return result
#
#
# def select_image():
#     Tk().withdraw()
#     file_path = filedialog.askopenfilename(title="选择图片", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
#     if file_path:
#         result = decode_qrcode_from_image(file_path)
#         if result:
#             print(f"[图片识别成功] 二维码内容为: {result}")
#         else:
#             print("[图片识别失败] 没有检测到二维码")
#
#
# def enhance_image(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
#     sharp = cv2.filter2D(gray, -1, sharpen_kernel)
#     return sharp
#
#
# def detect_and_decode_strict(image):
#     detector = cv2.QRCodeDetector()
#     gray = enhance_image(image)
#
#     # 二值化图像
#     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
#     # 膨胀让二维码边框连接得更清晰
#     kernel = np.ones((5, 5), np.uint8)
#     dilated = cv2.dilate(thresh, kernel, iterations=1)
#
#     # 寻找轮廓，尝试找出疑似二维码区域
#     contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]  # 只处理最大的几个区域
#
#     for cnt in contours:
#         x, y, w, h = cv2.boundingRect(cnt)
#         roi = image[y:y + h, x:x + w]
#         if roi.size < 500:  # 忽略太小的块
#             continue
#         data, _, _ = detector.detectAndDecode(roi)
#         if data:
#             return data  # 成功就返回
#     return None
#
#
# def scan_from_camera():
#     cap = cv2.VideoCapture(0)
#     print("🚀 启动摄像头扫码（按 Q 退出）")
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         data = detect_and_decode_strict(frame)
#         if data:
#             print(f"[✅ 识别成功] 二维码内容: {data}")
#             cv2.putText(frame, f"{data}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
#         else:
#             h, w = frame.shape[:2]
#             warning_text = "⚠️ 请将二维码移近摄像头"
#             cv2.putText(frame, warning_text, (int(w * 0.05), int(h * 0.95)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
#                         2)
#
#         cv2.imshow("摄像头扫码（按 Q 退出）", frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#
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






import cv2
from tkinter import filedialog, Tk
import numpy as np



def decode_qrcode_from_image(image_path):# 从图像路径读取并解码二维码的函数
    image = cv2.imread(image_path)                                              # 使用OpenCV的imread函数读取指定路径的图像
    result = detect_and_decode_strict(image)                                    # 调用自定义的严格检测和解码函数处理图像
    return result



def select_image(): # 打开文件选择对话框选择图像的函数
    Tk().withdraw()                                                             # 创建并隐藏tkinter主窗口（不需要完整的GUI界面）
    file_path = filedialog.askopenfilename(title="快来选择你的图片吧~~🚀", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])# 打开文件选择对话框，设置标题和允许的文件类型
    if file_path:                                                               # 如果用户选择了文件

        result = decode_qrcode_from_image(file_path)# 调用解码函数处理选中的图像

        if result:
            print(f"[图片识别成功] 已解码: {result}")# 如果成功检测到二维码内容
        else:
            print("图片好像有点小问题，没有识别到哎~~~")



def enhance_image(image):# 增强图像质量以便更好地检测二维码的函数
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                                              # 将BGR颜色空间的图像转换为灰度图像（减少颜色干扰）
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])                        # 定义锐化卷积核，用于增强图像边缘和细节
    sharp = cv2.filter2D(gray, -1, sharpen_kernel)                                              # 应用锐化卷积核对灰度图像进行滤波
    return sharp



def detect_and_decode_strict(image):# 严格检测和解码二维码的函数（尝试多种方法提高成功率）

    detector = cv2.QRCodeDetector()                                                             # 创建OpenCV的QR码检测器对象

    gray = enhance_image(image)                                                                 # 调用图像增强函数处理原始图像


    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)    # 对锐化后的灰度图像进行二值化处理（使用Otsu算法自动确定阈值）


    kernel = np.ones((5, 5), np.uint8)                                                      # 定义5x5的正方形结构元素，用于形态学操作

    dilated = cv2.dilate(thresh, kernel, iterations=1)                                            # 对二值图像进行膨胀操作，使二维码的边框更连续


    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)              # 在膨胀后的图像中查找轮廓（可能的物体边界）

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]                         # 按轮廓面积从大到小排序，只保留最大的10个轮廓


    for cnt in contours:# 遍历筛选后的轮廓

        x, y, w, h = cv2.boundingRect(cnt)                                                      # 计算轮廓的边界矩形（x,y为左上角坐标，w,h为宽高）

        roi = image[y:y + h, x:x + w]                                                           # 从原始图像中提取边界矩形区域的图像（感兴趣区域ROI）

        if roi.size < 500:                                                                      # 如果ROI区域太小（像素数少于500），认为不是有效二维码区域
            continue

        data, _, _ = detector.detectAndDecode(roi)                                              # 对ROI区域尝试检测和解码二维码

        if data:                                                                                # 如果成功解码出数据
            return data                                                                         # 立即返回解码结果

    return None




def scan_from_camera():# 从摄像头实时扫描二维码的函数

    cap = cv2.VideoCapture(0)                                                                   # 打开默认摄像头（设备ID为0）
    print("🚀 启动摄像头扫码（按 Q 退出）")


    while True:# 进入无限循环，持续获取摄像头帧并处理

        ret, frame = cap.read()                                                                 # 读取一帧图像，ret表示是否成功读取，frame是图像数据

        if not ret:                                                                             # 如果无法读取帧，退出循环
            break


        data = detect_and_decode_strict(frame)                                                  # 对当前帧应用严格检测和解码函数

        if data:# 如果成功检测到二维码内容
            print(f"[✅ 识别成功] 二维码内容: {data}")

            cv2.putText(frame, f"{data}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)# 在图像上绘制识别结果文本（绿色字体）
        else:

            h, w = frame.shape[:2]                                                              # 获取图像的高度和宽度

            warning_text = "⚠️ 请将二维码移近摄像头"                                                  # 设置提示文本（未检测到二维码）

            cv2.putText(frame, warning_text, (int(w * 0.05), int(h * 0.95)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)# 在图像底部绘制提示文本（红色字体）


        cv2.imshow("摄像头扫码（按 Q 退出）", frame)#                                         显示处理后的图像窗口

        if cv2.waitKey(1) & 0xFF == ord('q'):                                                   # 等待1毫秒，检测是否按下了'q'键（ASCII码为ord('q')）
            break


    cap.release()# 释放摄像头资源

    cv2.destroyAllWindows()# 关闭所有OpenCV创建的窗口


if __name__ == "__main__":
    print("选择功能：\n1 - 摄像头识别二维码\n2 - 上传图片识别二维码")
    # 获取用户输入并去除前后空格
    choice = input("请输入选项 (1 或 2): ").strip()

    if choice == '1':
        scan_from_camera()
    elif choice == '2':
        select_image()
    else:
        print("无效选项，请输入 1 或 2")

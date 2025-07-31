# main.py - 主应用文件
import os
import platform

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from PIL import Image as PILImage
import pytesseract
import numpy as np

# 设置中文字体支持
from kivy.core.text import LabelBase
from kivy.config import Config


class OCRApp(App):
    def build(self):
        # 设置中文字体
        project_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(project_dir, 'simhei.ttf')
        Config.set('kivy', 'default_font', ['SimHei', font_path])
        LabelBase.register(name='SimHei', fn_regular=font_path)

        # 动态设置 Tesseract 路径
        if platform.system() == 'Windows':
            pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'
        elif platform.system() == 'Linux':
            pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        elif platform.system() == 'Darwin':
            pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
        else:
            # Android 环境（打包后用）
            pytesseract.pytesseract.tesseract_cmd = '/data/data/org.example.yourapp/files/tesseract/tesseract'

        # 界面布局
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 摄像头组件
        self.camera = Camera(resolution=(640, 480), play=False)
        self.layout.add_widget(self.camera)

        # 控制按钮
        self.control_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        self.capture_btn = Button(
            text="拍照识别",
            size_hint=(0.5, 1),
            color=(0, 0, 0, 1),
            font_name='SimHei',
            font_size=20
        )
        self.capture_btn.bind(on_press=self.capture)

        self.live_btn = Button(
            text="实时识别",
            size_hint=(0.5, 1),
            color=(0, 0, 0, 1),
            font_name='SimHei',
            font_size=20,
            background_color=(0.7, 0.7, 0.7, 1)  # 默认置灰
        )
        self.live_btn.bind(on_press=self.toggle_live_ocr)

        self.control_layout.add_widget(self.capture_btn)
        self.control_layout.add_widget(self.live_btn)
        self.layout.add_widget(self.control_layout)

        # 结果显示
        self.result_label = Label(
            text="识别结果将显示在这里",
            font_name='SimHei',
            size_hint=(1, 0.3),
            color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.result_label)

        # 状态变量
        self.live_ocr_active = False
        self.ocr_interval = 1  # 每秒执行一次OCR
        self.last_recognized_text = ""  # 保存最后识别的文本

        return self.layout

    def toggle_live_ocr(self, instance):
        self.live_ocr_active = not self.live_ocr_active
        self.camera.play = self.live_ocr_active

        if self.live_ocr_active:
            self.live_btn.text = "停止识别"
            self.live_btn.background_color = (0.2, 0.6, 0.2, 1)  # 高亮（绿色）
            Clock.schedule_interval(self.perform_live_ocr, self.ocr_interval)
        else:
            self.live_btn.text = "实时识别"
            self.live_btn.background_color = (0.7, 0.7, 0.7, 1)  # 置灰
            Clock.unschedule(self.perform_live_ocr)

    def perform_live_ocr(self, dt):
        if self.camera.texture:
            # 获取当前摄像头帧
            texture = self.camera.texture
            size = texture.size
            pixels = texture.pixels

            # 转换为PIL图像
            img = PILImage.frombytes(mode='RGBA', size=size, data=pixels)
            img = img.convert('RGB')

            # 执行OCR
            text = self.perform_ocr(img)
            self.result_label.text = text

            # 如果识别到有效文本，显示确认弹窗
            if text.strip() and text != self.last_recognized_text:
                self.last_recognized_text = text
                self.show_confirmation_popup(text)

    def capture(self, instance):
        if self.camera.texture:
            # 拍照并保存
            img_name = "captured_image.jpg"
            self.camera.export_to_png(img_name)
            print(f"图片已保存至: {img_name}")

            # 打开图像进行OCR
            img = PILImage.open(img_name)

            # 执行OCR
            text = self.perform_ocr(img)
            self.result_label.text = text

    def perform_ocr(self, image):
        try:
            # 图像预处理
            img = image.convert('L')  # 灰度化
            img = img.point(lambda x: 0 if x < 128 else 255, '1')  # 二值化
            img = img.resize((img.width * 2, img.height * 2), PILImage.Resampling.BICUBIC)  # 放大

            # 执行OCR
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            print(f"OCR识别结果: {text}")
            return text
        except Exception as e:
            print(f"OCR错误: {str(e)}")
            return f"识别错误: {str(e)}"

    def show_confirmation_popup(self, text):
        # 创建确认弹窗
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 显示识别的文本
        text_label = Label(
            text=f"识别结果:\n\n{text}",
            font_name='SimHei',
            size_hint=(1, 0.8)
        )
        content.add_widget(text_label)

        # 确认按钮
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)

        confirm_btn = Button(
            text="确认",
            font_name='SimHei',
            background_color=(0.2, 0.6, 0.2, 1)  # 绿色
        )
        confirm_btn.bind(on_press=self.confirm_and_stop)

        cancel_btn = Button(
            text="取消",
            font_name='SimHei',
            background_color=(0.6, 0.2, 0.2, 1)  # 红色
        )
        cancel_btn.bind(on_press=lambda x: popup.dismiss())

        button_layout.add_widget(confirm_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)

        popup = Popup(
            title="确认识别结果",
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )
        popup.open()

    def confirm_and_stop(self, instance):
        # 确认后停止实时识别
        if self.live_ocr_active:
            self.toggle_live_ocr(None)

        # 关闭弹窗（需要先获取对弹窗的引用）
        # 这里简化处理，实际项目中可能需要更完善的实现
        instance.parent.parent.parent.dismiss()


if __name__ == '__main__':
    OCRApp().run()
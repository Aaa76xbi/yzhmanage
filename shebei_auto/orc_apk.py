# main.py - 主应用文件
import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.clock import Clock
from PIL import Image as PILImage
import pytesseract
import numpy as np
from kivy.core.image import Image as CoreImage
from io import BytesIO

# 设置中文字体支持
from kivy.core.text import LabelBase

LabelBase.register(name='SimHei', fn_regular='SimHei.ttf')  # 确保将字体文件放入项目目录


class OCRApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 摄像头组件
        self.camera = Camera(resolution=(640, 480), play=False)
        self.layout.add_widget(self.camera)

        # 控制按钮
        self.control_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        self.capture_btn = Button(text="拍照识别", size_hint=(0.5, 1))
        self.capture_btn.bind(on_press=self.capture)

        self.live_btn = Button(text="实时识别", size_hint=(0.5, 1))
        self.live_btn.bind(on_press=self.toggle_live_ocr)

        self.control_layout.add_widget(self.capture_btn)
        self.control_layout.add_widget(self.live_btn)

        self.layout.add_widget(self.control_layout)

        # 结果显示
        self.result_label = Label(text="识别结果将显示在这里", font_name='SimHei', size_hint=(1, 0.3))
        self.layout.add_widget(self.result_label)

        # 状态变量
        self.live_ocr_active = False
        self.ocr_interval = 1  # 每秒执行一次OCR

        # 设置Tesseract路径（Android上的路径）
        pytesseract.pytesseract.tesseract_cmd = '/data/data/org.example.yourapp/files/tesseract/tesseract'

        return self.layout

    def toggle_live_ocr(self, instance):
        self.live_ocr_active = not self.live_ocr_active
        self.camera.play = self.live_ocr_active

        if self.live_ocr_active:
            self.live_btn.text = "停止识别"
            Clock.schedule_interval(self.perform_live_ocr, self.ocr_interval)
        else:
            self.live_btn.text = "实时识别"
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

    def capture(self, instance):
        if self.camera.texture:
            # 拍照并保存
            img_name = "captured_image.jpg"
            self.camera.export_to_png(img_name)

            # 打开图像进行OCR
            img = PILImage.open(img_name)

            # 执行OCR
            text = self.perform_ocr(img)
            self.result_label.text = text

    def perform_ocr(self, image):
        try:
            # 执行OCR，指定中文语言包
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            return text
        except Exception as e:
            return f"识别错误: {str(e)}"


if __name__ == '__main__':
    OCRApp().run()
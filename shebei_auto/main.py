from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.clock import Clock
from PIL import Image
import pytesseract
import os


# 适配 Android 路径：/data/data/包名/files/
def get_android_path():
    from jnius import autoclass  # Buildozer 打包后自动支持
    Context = autoclass('android.content.Context')
    return Context.getFilesDir().getAbsolutePath()


class OCRApp(App):
    def build(self):
        # 初始化布局
        layout = BoxLayout(orientation='vertical', padding=20)

        # 摄像头组件
        self.camera = Camera(resolution=(640, 480), play=True)
        layout.add_widget(self.camera)

        # 按钮
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.capture_btn = Button(text="拍照识别")
        self.capture_btn.bind(on_press=self.capture)
        self.live_btn = Button(text="实时识别")
        self.live_btn.bind(on_press=self.toggle_live)
        btn_layout.add_widget(self.capture_btn)
        btn_layout.add_widget(self.live_btn)
        layout.add_widget(btn_layout)

        # 结果显示
        self.result = Label(text="识别结果", size_hint=(1, 0.3), font_name='Roboto')
        layout.add_widget(self.result)

        # 实时识别状态
        self.live_active = False
        return layout

    def capture(self, *args):
        # 拍照并保存
        self.camera.export_to_png("captured.png")
        # 调用 OCR
        text = self.do_ocr("captured.png")
        self.result.text = text

    def toggle_live(self, *args):
        self.live_active = not self.live_active
        if self.live_active:
            Clock.schedule_interval(self.live_ocr, 1)  # 每秒识别一次
            self.live_btn.text = "停止识别"
        else:
            Clock.unschedule(self.live_ocr)
            self.live_btn.text = "实时识别"

    def live_ocr(self, dt):
        # 从摄像头取帧转 PIL 图像
        texture = self.camera.texture
        image = Image.frombytes("RGBA", texture.size, texture.pixels).convert("RGB")
        text = self.do_ocr(image)
        self.result.text = text

    def do_ocr(self, image_path_or_obj):
        # 自动判断路径或 PIL 对象
        if isinstance(image_path_or_obj, str):
            image = Image.open(image_path_or_obj)
        else:
            image = image_path_or_obj

        # 关键：指定 Tesseract 路径和语言包目录
        try:
            # Android 路径适配
            if os.name == 'posix':  # 检测 Android 环境
                tesseract_cmd = os.path.join(get_android_path(), "tesseract")
                tessdata_dir = os.path.join(get_android_path(), "tessdata")
            else:  # 电脑调试环境
                tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'  # 替换你电脑的路径
                tessdata_dir = r'D:\Tesseract-OCR\tessdata'

            return pytesseract.image_to_string(
                image,
                lang='chi_sim+eng',
                config=f'--tessdata-dir "{tessdata_dir}"',
                cmd=tesseract_cmd
            ).strip()
        except Exception as e:
            return f"识别失败：{str(e)}"


if __name__ == '__main__':
    OCRApp().run()
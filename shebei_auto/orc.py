import pytesseract
from PIL import Image


def ocr_image(image_path):
    # 打开图片（支持JPG、PNG等格式）
    img = Image.open(image_path)

    # 调用Tesseract进行OCR识别
    # 如果Tesseract未添加到环境变量，需指定路径：pytesseract.pytesseract.tesseract_cmd = r'安装路径\tesseract.exe'
    text = pytesseract.image_to_string(img, lang='chi_sim')  # lang='chi_sim' 表示识别中文，默认英文

    return text


# 测试：替换为你的图片路径
if __name__ == '__main__':
    image_path = 'D:\pythonProject_mannageYZH\shebei_auto\image\9.jpg'  # 例如：一张包含文字的图片
    result = ocr_image(image_path)
    print("识别结果：")
    print(result)

# 示例调用
# 假设当前目录下有一张名为 test.png 的图片，运行后会输出识别到的文字
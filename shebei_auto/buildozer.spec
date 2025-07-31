[app]
title = OCRApp
package.name = ocr_app
package.domain = org.ocr
source.dir = .
version = 1.0
requirements = kivy,pillow,pytesseract,numpy,jnius
orientation = portrait
fullscreen = 0

[android]
android.api = 28
android.minapi = 21
android.sdk = 28
android.ndk = 25.2.9519653
source.include_exts = py,png,jpg,kv,atlas,ttf,traineddata,so
source.include_dirs = libs, tessdata
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.extra_libs = %(source.dir)s/libs/armeabi-v7a/*.so
android.assets = tessdata/
android.icon = icon.png
android.private_storage = True

[buildozer]
android.sdk_path = /home/adminxbj/android/sdk
android.make_args = -j 4
android.build_flags = --debug

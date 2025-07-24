#폰트 등록하기 윈도우 전용

import ctypes
import os

def add_font(font_path):
    FR_PRIVATE = 0x10
    path = os.path.abspath(font_path)
    if os.path.exists(path):
        ctypes.windll.gdi32.AddFontResourceExW(path, FR_PRIVATE, 0)
    else:
        raise FileNotFoundError(f"Font file not found: {path}")

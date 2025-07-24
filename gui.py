from tkinter import *
from PIL import Image, ImageTk
import random

def Click(event):
    userbox_x, userbox_y = 645, 550

    # 이미지 크기 가져오기 (실제 이미지 크기를 사용)
    bbox = canvas.bbox("userBox")  # userBox 태그가 붙은 이미지 영역 반환 (x1,y1,x2,y2)
    if bbox:
        x1, y1, x2, y2 = bbox
        # 클릭 위치가 아이템 박스 이미지 영역 내인지 체크
        if x1 <= event.x <= x2 and y1 <= event.y <= y2 :
            pass
        else:
            print(f"클릭 위치: x={event.x}, y={event.y} (아이템 박스 아님)")
    else:
        print("userBox 이미지 영역을 찾을 수 없습니다.")

# 인벤토리 슬롯 좌표 (왼쪽 인벤토리 2x2 기준)
inventory_slots = [
    (265, 457),
    (419, 450),
    (259, 566),
    (420, 564)
]

# 윈도우 초기화
window = Tk()
window.title("Buckshot Roulette")
window.geometry("1280x720")
window.iconbitmap("./image/Buckshot_Roulette.ico")

canvas = Canvas(window, width=1280, height=720, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# 배경 이미지
wall_photo = ImageTk.PhotoImage(Image.open("./image/wallpaper.png").convert("RGBA").resize((1280, 720)))
canvas.create_image(0, 0, image=wall_photo, anchor="nw")

# 게임 보드
board_photo = ImageTk.PhotoImage(Image.open("./image/game_board.png").convert("RGBA").resize((1280, 720)))
canvas.create_image(0, 0, image=board_photo, anchor="nw")

# 아이템 지급 이미지 참조 유지
loaded_item_images = []

# 아이템 캔버스 객체 태그 저장
selectedCanvasItems = []

# 아이템 지급 함수


# 전체 창 클릭 시 좌표 확인 및 아이템 박스 클릭 여부 체크
window.bind("<Button-1>", Click)

window.mainloop()

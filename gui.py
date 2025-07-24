from tkinter import *
from PIL import Image, ImageTk
import random

def Click(event):
    print(f"x = {event.x}, y = {event.y}")

class Item:
    def __init__(self, name):
        self.name = name

# 아이템 풀 정의
ItemPool = [
    Item("수갑"),
    Item("맥주"),
    Item("돋보기"),
    Item("담배"),
    Item("포티노"),
    Item("대포폰"),
    Item("변환기"),
    Item("아드레날린"),
    Item("상한 약")
]

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

# 아이템 이미지 등록 (100x100으로 크기 확대)
ItemImage = {
    "아이템박스": ImageTk.PhotoImage(Image.open("./image/ybox.png").resize((1280,720))),
    "수갑": ImageTk.PhotoImage(Image.open("./image/handcuffs.png").resize((1280,720))),
    "맥주": ImageTk.PhotoImage(Image.open("./image/beer.png").resize((1280,720))),
    "돋보기": ImageTk.PhotoImage(Image.open("./image/magnifying_glass.png").resize((1280,720))),
    "담배": ImageTk.PhotoImage(Image.open("./image/cigarette_pack.png").resize((1280,720))),
    "포티노": ImageTk.PhotoImage(Image.open("./image/hand_saw.png").resize((1280,720))),
    "대포폰": ImageTk.PhotoImage(Image.open("./image/phone.png").resize((1280,720))),
    "변환기": ImageTk.PhotoImage(Image.open("./image/inverter.png").resize((1280,720))),
    "아드레날린": ImageTk.PhotoImage(Image.open("./image/adrenaline.png").resize((1280,720))),
    "상한 약": ImageTk.PhotoImage(Image.open("./image/medicine.png").resize((1280,720)))
}

# 아이템 지급 이미지 참조 유지
loaded_item_images = []

# 아이템 캔버스 객체 태그 저장
selectedCanvasItems = []

# 아이템 지급 함수
def BoxClick(event=None):
    global selectedCanvasItems, loaded_item_images

    # 기존 아이템 삭제
    for tag in selectedCanvasItems:
        canvas.delete(tag)
    selectedCanvasItems.clear()
    loaded_item_images.clear()

    # 랜덤 아이템 2개 선택 (중복 허용)
    selectedItems = [random.choice(ItemPool) for _ in range(2)]

    # 이미지 띄우기 (왼쪽 인벤토리 슬롯에 삽입)
    for i, item in enumerate(selectedItems):
        x, y = inventory_slots[i]
        img = ItemImage[item.name]
        tag = f"user_item_{i}"
        canvas.create_image(x, y, image=img, anchor="center", tags=tag)
        selectedCanvasItems.append(tag)
        loaded_item_images.append(img)

    print("아이템 지급됨:", [item.name for item in selectedItems])

# 유저 아이템박스
userBox_photo = ImageTk.PhotoImage(
    Image.open("./image/ybox.png").convert("RGBA").resize((1280, 720)))
canvas.create_image(645, 550, image=userBox_photo, anchor="center", tags="userBox")
canvas.tag_bind("userBox", "<Button-1>", BoxClick)


window.bind("<Button-1>", Click)
window.mainloop()

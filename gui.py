from tkinter import *
from PIL import Image, ImageTk
import random

def Click(event):
    # 아이템 박스 이미지가 캔버스에 그려진 위치와 크기
    userbox_x, userbox_y = 645, 550

    # 이미지 크기 가져오기 (실제 이미지 크기를 사용)
    bbox = canvas.bbox("userBox")  # userBox 태그가 붙은 이미지 영역 반환 (x1,y1,x2,y2)
    if bbox:
        x1, y1, x2, y2 = bbox
        # 클릭 위치가 아이템 박스 이미지 영역 내인지 체크
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            BoxClick()
        else:
            print(f"클릭 위치: x={event.x}, y={event.y} (아이템 박스 아님)")
    else:
        print("userBox 이미지 영역을 찾을 수 없습니다.")

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

# 아이템 이미지 등록 (원본 크기 유지)
ItemImage = {
    "아이템박스": ImageTk.PhotoImage(Image.open("./image/ybox.png").convert("RGBA")),
    "수갑": ImageTk.PhotoImage(Image.open("./image/handcuffs.png").convert("RGBA")),
    "맥주": ImageTk.PhotoImage(Image.open("./image/beer.png").convert("RGBA")),
    "돋보기": ImageTk.PhotoImage(Image.open("./image/magnifying_glass.png").convert("RGBA")),
    "담배": ImageTk.PhotoImage(Image.open("./image/cigarette_pack.png").convert("RGBA")),
    "포티노": ImageTk.PhotoImage(Image.open("./image/hand_saw.png").convert("RGBA")),
    "대포폰": ImageTk.PhotoImage(Image.open("./image/phone.png").convert("RGBA")),
    "변환기": ImageTk.PhotoImage(Image.open("./image/inverter.png").convert("RGBA")),
    "아드레날린": ImageTk.PhotoImage(Image.open("./image/adrenaline.png").convert("RGBA")),
    "상한 약": ImageTk.PhotoImage(Image.open("./image/medicine.png").convert("RGBA"))
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

# 유저 아이템박스 (원본 이미지 크기 유지)
userBox_photo = ItemImage["아이템박스"]
canvas.create_image(645, 550, image=userBox_photo, anchor="center", tags="userBox")

# 전체 창 클릭 시 좌표 확인 및 아이템 박스 클릭 여부 체크
window.bind("<Button-1>", Click)

window.mainloop()

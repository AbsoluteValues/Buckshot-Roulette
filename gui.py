from tkinter import *
from PIL import Image, ImageTk
import random

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    left = max((img_width - crop_width) // 2, 0)
    top = max((img_height - crop_height) // 2, 0)
    right = left + crop_width
    bottom = top + crop_height
    return pil_img.crop((left, top, right, bottom))

# 아이템 클래스 정의
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

# 인벤토리 슬롯 좌표 8개 (x, y)
inventory_slots = [
    (265, 457),
    (419, 450),
    (837, 446),
    (1007, 448),
    (259, 566),
    (420, 564),
    (833, 570),
    (996, 569)
]

window = Tk()
window.title("Buckshot Roulette")
window.geometry("1280x720")
window.iconbitmap("./image/Buckshot_Roulette.ico")

canvas = Canvas(window, width=1280, height=720, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# 배경 이미지 (가장 아래, 크롭 없이 원본 크기)
wall_photo = ImageTk.PhotoImage(Image.open("./image/wallpaper.png").convert("RGBA").resize((1280, 720)))
canvas.create_image(0, 0, image=wall_photo, anchor="nw")

# 게임 보드 (배경 위, 크롭 없이 원본 크기)
board_photo = ImageTk.PhotoImage(Image.open("./image/game_board.png").convert("RGBA").resize((1280, 720)))
canvas.create_image(0, 0, image=board_photo, anchor="nw")

# ybox 이미지 (핑크 박스 위치에 표시, 크롭 없이 300x300으로 리사이즈)
ybox_img = Image.open("./image/ybox.png").convert("RGBA").resize((300, 300))
ybox_photo = ImageTk.PhotoImage(ybox_img)

# 아이템 이미지 등록 (배경, 보드, ybox 제외, 아이템만 중앙 720x720 크롭)
ItemImage = {
    "수갑": ImageTk.PhotoImage(crop_center(Image.open("./image/handcuffs.png").convert("RGBA"), 450, 450)),
    "맥주": ImageTk.PhotoImage(crop_center(Image.open("./image/beer.png").convert("RGBA"), 450, 450)),
    "돋보기": ImageTk.PhotoImage(crop_center(Image.open("./image/magnifying_glass.png").convert("RGBA"), 450, 450)),
    "담배": ImageTk.PhotoImage(crop_center(Image.open("./image/cigarette_pack.png").convert("RGBA"), 450, 450)),
    "포티노": ImageTk.PhotoImage(crop_center(Image.open("./image/hand_saw.png").convert("RGBA"), 450, 450)),
    "대포폰": ImageTk.PhotoImage(crop_center(Image.open("./image/phone.png").convert("RGBA"), 450, 450)),
    "변환기": ImageTk.PhotoImage(crop_center(Image.open("./image/inverter.png").convert("RGBA"), 450, 450)),
    "아드레날린": ImageTk.PhotoImage(crop_center(Image.open("./image/adrenaline.png").convert("RGBA"), 450, 450)),
    "상한 약": ImageTk.PhotoImage(crop_center(Image.open("./image/medicine.png").convert("RGBA"), 450, 450))
}

# 이미지 참조 저장용 리스트
loaded_item_images = []

pink_box_pos = (645, 550)

current_item = None
current_item_img = None
current_item_canvas_id = None
current_item_slot = None  # None: 핑크 박스 위, 0~7: 슬롯 번호

def BoxClick(event=None):
    global current_item, current_item_img, current_item_canvas_id, current_item_slot
    
    if current_item is not None:
        print("이미 아이템이 있습니다! 슬롯 중 하나를 클릭하세요.")
        return
    
    current_item = random.choice(ItemPool)
    current_item_img = ItemImage[current_item.name]
    current_item_canvas_id = canvas.create_image(pink_box_pos[0], pink_box_pos[1], image=current_item_img, anchor="center")
    loaded_item_images.append(current_item_img)
    current_item_slot = None
    print(f"아이템 지급됨: {current_item.name}")

def SlotClick(event):
    global current_item_canvas_id, current_item_slot
    
    if current_item is None:
        print("먼저 핑크 박스를 클릭해 아이템을 받아야 합니다.")
        return
    
    x, y = event.x, event.y
    
    for idx, (slot_x, slot_y) in enumerate(inventory_slots):
        left = slot_x - 50
        right = slot_x + 50
        top = slot_y - 50
        bottom = slot_y + 50
        
        if left <= x <= right and top <= y <= bottom:
            canvas.coords(current_item_canvas_id, slot_x, slot_y)
            current_item_slot = idx
            print(f"아이템 '{current_item.name}'이(가) 슬롯 {idx + 1} 위치로 이동됨")
            return

# 슬롯 위치에 완전 투명 클릭 영역 이미지 생성 및 바인딩
slot_rects = []
for idx, (x, y) in enumerate(inventory_slots):
    transparent_slot_img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))  # 완전 투명 100x100 이미지
    transparent_slot_photo = ImageTk.PhotoImage(transparent_slot_img)
    loaded_item_images.append(transparent_slot_photo)

    slot_img_id = canvas.create_image(x, y, image=transparent_slot_photo, anchor="center", tags=f"slot_{idx}")
    canvas.tag_bind(f"slot_{idx}", "<Button-1>", SlotClick)


# ybox 이미지 (핑크 박스 위치, 보드 위, 슬롯 파란 네모 아래)
canvas.create_image(pink_box_pos[0], pink_box_pos[1], image=ybox_photo, anchor="center", tags="ybox")

# 핑크 박스 클릭 영역 완전 투명 이미지로 변경
pink_img = Image.new("RGBA", (170, 170), (0, 0, 0, 0))  # 완전 투명 박스
pink_square_photo = ImageTk.PhotoImage(pink_img)
pink_area_id = canvas.create_image(pink_box_pos[0], pink_box_pos[1], image=pink_square_photo, anchor="center", tags="pinkBoxArea")
loaded_item_images.append(pink_square_photo)
canvas.tag_bind("pinkBoxArea", "<Button-1>", BoxClick)



window.mainloop()

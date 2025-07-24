from tkinter import *
from PIL import Image, ImageTk
import random
import gun

item_list = []  # 최대 두 개의 아이템을 저장
item_index = 0  # 현재 소환된 아이템 인덱스 (0 또는 1)

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    left = max((img_width - crop_width) // 2, 0)
    top = max((img_height - crop_height) // 2, 0)
    right = left + crop_width
    bottom = top + crop_height
    return pil_img.crop((left, top, right, bottom))

class Item:
    def __init__(self, name):
        self.name = name

ItemPool = [
    Item("수갑"), Item("맥주"), Item("돋보기"), Item("담배"),
    Item("포티노"), Item("대포폰"), Item("변환기"),
    Item("아드레날린"), Item("상한 약")
]

inventory_slots = [
    (265, 457), (419, 450), (837, 446), (1007, 448),
    (259, 566), (420, 564), (833, 570), (996, 569)
]

window = Tk()
window.title("Buckshot Roulette")
window.geometry("1280x720")
window.iconbitmap("./image/Buckshot_Roulette.ico")

canvas = Canvas(window, width=1280, height=720, highlightthickness=0)
canvas.pack(fill="both", expand=True)

wall_photo = ImageTk.PhotoImage(Image.open("./image/wallpaper.png").convert("RGBA").resize((1280, 720)))
canvas.create_image(0, 0, image=wall_photo, anchor="nw")

board_photo = ImageTk.PhotoImage(Image.open("./image/game_board.png").convert("RGBA").resize((1280, 720)))
canvas.create_image(0, 0, image=board_photo, anchor="nw")

# ybox 이미지 준비 및 캔버스에 배치
ybox_raw = Image.open("./image/ybox.png").convert("RGBA")
ybox_cropped = crop_center(ybox_raw, 600, 600).resize((225, 225), Image.Resampling.LANCZOS)
ybox_photo = ImageTk.PhotoImage(ybox_cropped)
pink_box_pos = (645, 550)
ybox_id = canvas.create_image(pink_box_pos[0], pink_box_pos[1], image=ybox_photo, anchor="center", tags="ybox")

# 🟩 gun.py의 setup_shotgun 호출 시 ybox_id도 전달
gun.setup_shotgun(canvas, window, ybox_id)

ItemImage = {
    "수갑": ImageTk.PhotoImage(crop_center(Image.open("./image/handcuffs.png").convert("RGBA"), 400, 400)),
    "맥주": ImageTk.PhotoImage(crop_center(Image.open("./image/beer.png").convert("RGBA"), 400, 400)),
    "돋보기": ImageTk.PhotoImage(crop_center(Image.open("./image/magnifying_glass.png").convert("RGBA"), 400, 400)),
    "담배": ImageTk.PhotoImage(crop_center(Image.open("./image/cigarette_pack.png").convert("RGBA"), 400, 400)),
    "포티노": ImageTk.PhotoImage(crop_center(Image.open("./image/hand_saw.png").convert("RGBA"), 400, 400)),
    "대포폰": ImageTk.PhotoImage(crop_center(Image.open("./image/phone.png").convert("RGBA"), 400, 400)),
    "변환기": ImageTk.PhotoImage(crop_center(Image.open("./image/inverter.png").convert("RGBA"), 400, 400)),
    "아드레날린": ImageTk.PhotoImage(crop_center(Image.open("./image/adrenaline.png").convert("RGBA"), 400, 400)),
    "상한 약": ImageTk.PhotoImage(crop_center(Image.open("./image/medicine.png").convert("RGBA"), 400, 400))
}

loaded_item_images = []
current_item = None
current_item_img = None
current_item_canvas_id = None
current_item_slot = None

def BoxClick(event=None):
    global current_item, current_item_img, current_item_canvas_id, current_item_slot, item_list, item_index

    if item_index >= 2 or current_item is not None:
        return

    current_item = random.choice(ItemPool)
    current_item_img = ItemImage[current_item.name]
    current_item_canvas_id = canvas.create_image(pink_box_pos[0], pink_box_pos[1], image=current_item_img, anchor="center")
    loaded_item_images.append(current_item_img)
    current_item_slot = None
    item_list.append(current_item)

def SlotClick(event):
    global current_item_canvas_id, current_item_slot, current_item, item_index

    if current_item is None or current_item_slot is not None:
        return

    x, y = event.x, event.y
    for idx, (slot_x, slot_y) in enumerate(inventory_slots):
        if slot_x - 50 <= x <= slot_x + 50 and slot_y - 50 <= y <= slot_y + 50:
            canvas.coords(current_item_canvas_id, slot_x, slot_y)
            current_item_slot = idx
            current_item = None
            current_item_img = None
            current_item_canvas_id = None
            current_item_slot = None
            item_index += 1
            return

for idx, (x, y) in enumerate(inventory_slots):
    transparent_slot_img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    transparent_slot_photo = ImageTk.PhotoImage(transparent_slot_img)
    loaded_item_images.append(transparent_slot_photo)
    slot_img_id = canvas.create_image(x, y, image=transparent_slot_photo, anchor="center", tags=f"slot_{idx}")
    canvas.tag_bind(f"slot_{idx}", "<Button-1>", SlotClick)

# 핑크 박스 클릭 영역
pink_img = Image.new("RGBA", (170, 170), (0, 0, 0, 0))
pink_square_photo = ImageTk.PhotoImage(pink_img)
pink_area_id = canvas.create_image(pink_box_pos[0], pink_box_pos[1], image=pink_square_photo, anchor="center", tags="pinkBoxArea")
loaded_item_images.append(pink_square_photo)
canvas.tag_bind("pinkBoxArea", "<Button-1>", BoxClick)

window.mainloop()

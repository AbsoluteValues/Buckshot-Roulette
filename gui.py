from tkinter import *
from PIL import Image, ImageTk
import random
import gun
import hp

# 이미지 중앙 자르기 함수
def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    left = max((img_width - crop_width) // 2, 0)
    top = max((img_height - crop_height) // 2, 0)
    right = left + crop_width
    bottom = top + crop_height
    return pil_img.crop((left, top, right, bottom))

# 아이템 클래스
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

# 배경화면 및 게임보드 이미지 표시
wall_photo = ImageTk.PhotoImage(Image.open("./image/wallpaper.png").convert("RGBA").resize((1280, 720)))
canvas.create_image(0, 0, image=wall_photo, anchor="nw")

board_photo = ImageTk.PhotoImage(Image.open("./image/game_board.png").convert("RGBA").resize((1280, 720)))
canvas.create_image(0, 0, image=board_photo, anchor="nw")

# ybox 이미지 준비 및 배치
ybox_raw = Image.open("./image/ybox.png").convert("RGBA")
ybox_cropped = crop_center(ybox_raw, 600, 600).resize((225, 225), Image.Resampling.LANCZOS)
ybox_photo = ImageTk.PhotoImage(ybox_cropped)
pink_box_pos = (645, 550)
ybox_id = canvas.create_image(pink_box_pos[0], pink_box_pos[1], image=ybox_photo, anchor="center", tags="ybox")

gun.setup_shotgun(canvas, window, ybox_id)

# 아이템 이미지 딕셔너리
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
item_list = []
item_index = 0

# HPManager 생성 및 초기 체력 표시
#player_hp = 6
#dealer_hp = 6
#hp_manager = hp.HPManager(canvas)
# hp_manager.draw(player_hp=player_hp, dealer_hp=dealer_hp)

# 아이템 소환 박스 클릭 함수
def BoxClick(event=None):
    global current_item, current_item_img, current_item_canvas_id, current_item_slot, item_list, item_index

    if item_index >= 2 or current_item is not None:
        return

    current_item = random.choice(ItemPool)
    current_item_img = ItemImage[current_item.name]
    current_item_canvas_id = canvas.create_image(pink_box_pos[0], 
        pink_box_pos[1], image=current_item_img, anchor="center")
    loaded_item_images.append(current_item_img)
    current_item_slot = None
    item_list.append(current_item)

# 인벤토리 슬롯 클릭 함수
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

# 인벤토리 슬롯 투명 이미지 및 클릭 영역 생성
for idx, (x, y) in enumerate(inventory_slots):
    transparent_slot_img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    transparent_slot_photo = ImageTk.PhotoImage(transparent_slot_img)
    loaded_item_images.append(transparent_slot_photo)
    slot_img_id = canvas.create_image(x, y, image=transparent_slot_photo, anchor="center", tags=f"slot_{idx}")
    canvas.tag_bind(f"slot_{idx}", "<Button-1>", SlotClick)

# 핑크 박스 클릭 감지용 투명 이미지 (ybox 위 클릭 영역 생성)
pink_click_area = Image.new("RGBA", (170, 170), (0, 0, 0, 0))  # 완전히 투명한 이미지
pink_click_photo = ImageTk.PhotoImage(pink_click_area)
loaded_item_images.append(pink_click_photo)  # 참조 유지

# 캔버스에 클릭 감지 이미지 올리기
pink_area_id = canvas.create_image(
    pink_box_pos[0], pink_box_pos[1],
    image=pink_click_photo,
    anchor="center",
    tags="pinkBoxArea"
)

# 클릭 이벤트 바인딩 → 핑크 박스 클릭 시 BoxClick 함수 실행
canvas.tag_bind("pinkBoxArea", "<Button-1>", BoxClick)

window.mainloop()
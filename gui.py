import csv
from tkinter import *
from PIL import Image, ImageTk
import random

def Click(event) :
    print(f"x = {event.x}, y={event.y}") # 코드랑 마무리단계에서 익선이 어머니 곁으로 보내줘야함
    
selecteCanvasItems = []

ItemPool = [
    HandCuffs(),
    Beer(),
    MagnifyingGlass(),
    Cigarret(),
    ChainsawTino(),
    Phone(),
    Inverter(),
    Adrenaline(),
    Drug()
]

ItemImage = {
    "수갑": ImageTk.PhotoImage(Image.open("./image/handcuffs.png").resize((80, 80))),
    "맥주": ImageTk.PhotoImage(Image.open("./image/beer.png").resize((80, 80))),
    "돋보기": ImageTk.PhotoImage(Image.open("./image/magnifying_glass.png").resize((80, 80))),
    "담배": ImageTk.PhotoImage(Image.open("./image/cigarette_pack.png").resize((80, 80))),
    "포티노": ImageTk.PhotoImage(Image.open("./image/hand_saw.png").resize((80, 80))),
    "대포폰": ImageTk.PhotoImage(Image.open("./image/phone.png").resize((80, 80))),
    "변환기": ImageTk.PhotoImage(Image.open("./image/inverter.png").resize((80, 80))),
    "아드레날린": ImageTk.PhotoImage(Image.open("./image/adrenaline.png").resize((80, 80))),
    "상한 약": ImageTk.PhotoImage(Image.open("./image/medicine.png").resize((80, 80)))
}


def BoxClick() :
    global selcetCanvasItems
    selcetCanvasItems.clear()
    
    selectItems = [random.choice(ItemPool) for _ in range(2)]
    
    for i, item in enumerate(selectItems) :
        x = 100 + i * 120
        y = 500
        img = ItemImage[item.name]
        tag = f"item_{i}" 
        canvas.create_image(x, y, image=img, anchor="nw", tags=tag)
        selecteCanvasItems.append(tag)
    
window = Tk()
window.title("Buckshot Roulette")
window.geometry("1280x720")
window.iconbitmap("./image/Buckshot_Roulette.ico")

canvas = Canvas(window, width=1280, height=720, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# 배경 이미지
wall_image = Image.open("./image/wallpaper.png").convert("RGBA").resize((1280, 720))
wall_photo = ImageTk.PhotoImage(wall_image)
canvas.create_image(0, 0, image=wall_photo, anchor="nw")

# 보드 이미지
board_image = Image.open("./image/game_board.png").convert("RGBA").resize((1280, 720))
board_photo = ImageTk.PhotoImage(board_image)
canvas.create_image(0, 0, image=board_photo, anchor="nw")

# 유저 아이템박스
userBox_image = Image.open("./image/ybox.png").convert("RGBA").resize((1280, 720))
userBox_photo = ImageTk.PhotoImage(userBox_image)
canvas.create_image(645, 550, image=userBox_photo, anchor="center")

# 투명 PNG (Beer)
beer_image = Image.open("./image/beer.png").convert("RGBA").resize((1280, 720))
beer_photo = ImageTk.PhotoImage(beer_image)
canvas.create_image(100, 100, image=beer_photo, anchor="nw")

# 담배
cigarettePack_image = Image.open("./image/cigarette_pack.png").convert("RGBA").resize((1280, 720))
cigarettePack_photo = ImageTk.PhotoImage(cigarettePack_image)
canvas.create_image(100, 200, image=cigarettePack_photo, anchor="nw")

# 톱
HandSaw_image = Image.open("./image/hand_saw.png").convert("RGBA").resize((1280, 720))
HandSaw_photo = ImageTk.PhotoImage(HandSaw_image)
canvas.create_image(100, 200, image=HandSaw_photo, anchor="nw")

# 변환기
inverter_image = Image.open("./image/inverter.png").convert("RGBA").resize((1280, 720))
inverter_Photo = ImageTk.PhotoImage(inverter_image)
canvas.create_image(100, 200, image=inverter_Photo, anchor="nw")

# 돋보기
magnifying_image = Image.open("./image/magnifying_glass.png").convert("RGBA").resize((1280, 720))
magnifying_photo = ImageTk.PhotoImage(magnifying_image)
canvas.create_image(100, 200, image=magnifying_photo, anchor="nw")

# 돋보기(사용후)
magnifying2_image = Image.open("./image/magnifying_glass2.png").convert("RGBA").resize((1280, 720))
magnifying2_Photo = ImageTk.PhotoImage(magnifying2_image)
canvas.create_image(100, 200, image=inverter_Photo, anchor="nw")

# 대포폰
phone_image = Image.open("./image/phone.png").convert("RGBA").resize((1280, 720))
phone_photo = ImageTk.PhotoImage(phone_image)
canvas.create_image(100, 200, image=phone_photo, anchor="nw")

# 대포폰
phone_image = Image.open("./image/phone.png").convert("RGBA").resize((1280, 720))
phone_photo = ImageTk.PhotoImage(phone_image)
canvas.create_image(100, 200, image=phone_photo, anchor="nw")

# 약
medicine_image = Image.open("./image/medicine.png").convert("RGBA").resize((1280, 720))
medicine_photo = ImageTk.PhotoImage(medicine_image)
canvas.create_image(100, 200, image=medicine_photo, anchor="nw")


window.bind("<Button-1>",Click)
window.mainloop()
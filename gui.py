import csv
from tkinter import *
from PIL import Image, ImageTk

def Click(event) :
    print(f"x = {event.x}, y={event.y}")

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

# 투명 PNG (Beer)
beer_image = Image.open("./image/beer.png").convert("RGBA").resize((1280, 720))
beer_photo = ImageTk.PhotoImage(beer_image)
canvas.create_image(100, 100, image=beer_photo, anchor="nw")

# 유저 아이템박스
userBox_image = Image.open("./image/ybox.png").convert("RGBA").resize((1280, 720))
userBox_photo = ImageTk.PhotoImage(userBox_image)
canvas.create_image(645, 550, image=userBox_photo, anchor="center")


window.bind("<Button-1>",Click)
window.mainloop()
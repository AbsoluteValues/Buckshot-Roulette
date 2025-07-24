import csv
from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.title("Buckshot Roulette")
window.geometry("1280x720")

window.iconbitmap("./image/Buckshot_Roulette.ico") #게임 아이콘 변경 
# 경로를 이렇게 지정하는게 맞는지 모르겟음 수정 필요 

#배경화면 
wall_image_path = ("./image/wallpaper.png")
wall_image = Image.open(wall_image_path).convert("RGBA").resize((1280, 720))

wall_photo = ImageTk.PhotoImage(wall_image)

wall_label = Label(window, image=wall_photo)
wall_label.place(x=0, y=0, relwidth=1, relheight=1)

#게임 플레이 화면 (게임 보드 판)
board_image_path = ("./image/game_board.png")
board_image = Image.open(board_image_path)
board_image = board_image.resize((1280, 720))
board_photo = ImageTk.PhotoImage(board_image)

board_label = Label(window, image=board_photo)
board_label.place(x=0, y=0, relwidth=1, relheight=1)

ItemBeerImg = Image.open("./image/beer.png").convert("RGBA").resize((100, 100))
BeerImg = ImageTk.PhotoImage(ItemBeerImg)

ItemBeerImg_label1 = Label(window, image = BeerImg, bd = 0)
ItemBeerImg_label1.image = BeerImg
ItemBeerImg_label1.pack()


window.mainloop()
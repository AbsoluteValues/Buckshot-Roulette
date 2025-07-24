from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import subprocess 
from font_win import add_font # font_win.py 에서 불러오기 

add_font("Boucherie-Block.ttf")

window = Tk()
window.title("Buckshot Roulette")
window.geometry("1280x720")
window.iconbitmap("./image/Buckshot_Roulette.ico")

#폰트설정
custom_font = font.Font(family= "Boucherie Block", size=100) #글씨크기
button_font = font.Font(family= "Boucherie Block", size=40) 

canvas = Canvas(window, width=1280, height=720, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# 배경 이미지
wall_image = Image.open("./image/wallpaper.png").convert("RGBA").resize((1280, 720))
wall_photo = ImageTk.PhotoImage(wall_image)
canvas.create_image(0, 0, image=wall_photo, anchor="nw")

#피 배경
blood_image = Image.open("./image/title_blood.png").convert("RGBA").resize((1280, 720))
blood_photo = ImageTk.PhotoImage(blood_image)
canvas.create_image(0, 0, image=blood_photo, anchor="nw")


#제목 텍스트 위치 
canvas.create_text(640, 200, text="Buckshot Roulette", font=custom_font, fill="white", anchor="center")

#메뉴 3개 
def start_game():
    window.destroy()  # 현재 창 닫기
    subprocess.Popen(["python", "gui.py"])

def mode () :
    print("Mode")

def exit_game():
    window.destroy()

#버튼 생성  텍스트, 글꼴, 실행할 함수, 버튼 가로, 외각선, 강조 테두리, 배경색, 글자색, 눌렀을때 2개 
btn_start = Button(window, text="Game Start", font=button_font,command=start_game,width=12,
   bd=0,highlightthickness=0,bg="black",fg="white",activebackground="gray20",activeforeground="white")
btn_mode = Button(window, text="Mode", font=button_font, command=mode, width=10,
    bd=0,highlightthickness=0,bg="black",fg="white",activebackground="gray20",activeforeground="white")
btn_exit = Button(window, text="Exit", font=button_font, command=exit_game, width=10,
    bd=0,highlightthickness=0,bg="black",fg="white",activebackground="gray20",activeforeground="white")

#버튼 위치 
btn_start.place(x=640, y=340, anchor="center")
btn_mode.place(x=640, y=465, anchor="center")
btn_exit.place(x=640, y=590, anchor="center")


window.mainloop()

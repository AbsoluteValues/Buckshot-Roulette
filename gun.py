from tkinter import Button, font
from PIL import Image, ImageTk
from font_win import add_font

def setup_shotgun(canvas, root, ybox_id):
    add_font("Boucherie-Block.ttf")

    shotgun_img = ImageTk.PhotoImage(Image.open("./image/gun/shotgun.png").convert("RGBA"))
    shotgun_id = canvas.create_image(640, 360, image=shotgun_img, anchor="center")

    canvas.shotgun_img = shotgun_img
    canvas.shotgun_id = shotgun_id

    custom_font = font.Font(root=root, family="Boucherie Block", size=20)

    btn_dealer = Button(root, text="dealer", font=custom_font, padx=10, pady=5)
    btn_user = Button(root, text="user", font=custom_font, padx=10, pady=5)

    def on_dealer():
        aiming_img = ImageTk.PhotoImage(Image.open("./image/gun/shotgun_aiming.png").convert("RGBA"))
        canvas.itemconfig(shotgun_id, image=aiming_img)
        canvas.shotgun_img = aiming_img

    def on_user():
        aimed_img = ImageTk.PhotoImage(Image.open("./image/gun/shotgun_aimed.png").convert("RGBA"))
        canvas.itemconfig(shotgun_id, image=aimed_img)
        canvas.shotgun_img = aimed_img

    btn_dealer.config(command=on_dealer)
    btn_user.config(command=on_user)

    btn_dealer.place_forget()
    btn_user.place_forget()

    buttons_visible = [False]

    def toggle_buttons(event):
        if buttons_visible[0]:
            btn_dealer.place_forget()
            btn_user.place_forget()
            buttons_visible[0] = False
        else:
            btn_dealer.place(x=640 - 250, y=330)
            btn_user.place(x=640 + 110, y=330)
            buttons_visible[0] = True

            # 💥 ybox 이미지 삭제
            canvas.delete(ybox_id)

    canvas.tag_bind(shotgun_id, "<Button-1>", toggle_buttons)

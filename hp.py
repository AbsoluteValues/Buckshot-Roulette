# hp.py
from PIL import Image, ImageTk
import threading
import time

def load_heart_images():
    hearts = [ImageTk.PhotoImage(Image.open(f"image/hp/heart{i}.png").resize((120, 120))) for i in range(1, 7)]
    background = ImageTk.PhotoImage(Image.open("image/hp/heart_background.png").resize((140, 140)))
    return hearts, background

def draw_hearts(canvas, player_hp, dealer_hp):
    hearts, bg = load_heart_images()

    # 좌측 상단 (플레이어)
    canvas.player_heart_bg = canvas.create_image(50, 50, image=bg, anchor="nw")
    canvas.player_heart = canvas.create_image(60, 60, image=hearts[player_hp - 1], anchor="nw")

    # 우측 하단 (딜러)
    canvas.dealer_heart_bg = canvas.create_image(1080, 540, image=bg, anchor="nw")
    canvas.dealer_heart = canvas.create_image(1090, 550, image=hearts[dealer_hp - 1], anchor="nw")

    # 이미지 보존
    canvas.hp_images = hearts
    canvas.hp_background = bg

def update_hp(canvas, who, hp):
    hp = max(1, min(6, hp))  # 1~6 범위 제한
    image = canvas.hp_images[hp - 1]

    if who == "player":
        canvas.itemconfig(canvas.player_heart, image=image)
    elif who == "dealer":
        canvas.itemconfig(canvas.dealer_heart, image=image)

def shake_heart(canvas, who):
    target = canvas.player_heart if who == "player" else canvas.dealer_heart

    def animate():
        for dx in [-5, 5, -5, 5, 0]:
            canvas.move(target, dx, 0)
            time.sleep(0.05)

    threading.Thread(target=animate).start()

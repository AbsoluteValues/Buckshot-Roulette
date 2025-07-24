from PIL import Image, ImageTk
import threading
import time

class HPManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.player_hp = 6
        self.dealer_hp = 6
        self.hearts = []
        self.load_images()
        self.player_bg_id = None
        self.player_heart_id = None
        self.dealer_bg_id = None
        self.dealer_heart_id = None

    def load_images(self):
        self.hearts = []
        # 체력 이미지 6단계 로드 (크기 600x360 -> 2배 확대)
        for i in range(1, 7):
            img = Image.open(f"image/hp/heart{i}.png").resize((600, 360))
            self.hearts.append(ImageTk.PhotoImage(img))

        # 배경 이미지 (크기 600x400 -> 2배 확대)
        bg_img = Image.open("image/hp/heart_background.png").resize((600, 400))
        self.background = ImageTk.PhotoImage(bg_img)

    def draw(self, player_hp=None, dealer_hp=None):
        if player_hp is not None:
            self.player_hp = max(1, min(6, player_hp))
        if dealer_hp is not None:
            self.dealer_hp = max(1, min(6, dealer_hp))

        canvas_width = int(self.canvas['width'])
        canvas_height = int(self.canvas['height'])

        # 🎯 왼쪽 상단 모서리에 딱 맞게 배경 표시
        if self.player_bg_id is None:
            self.player_bg_id = self.canvas.create_image(0, 0, image=self.background, anchor="nw")
        else:
            self.canvas.itemconfig(self.player_bg_id, image=self.background)

        # 🎯 오른쪽 상단 모서리에 딱 맞게 배경 표시
        if self.dealer_bg_id is None:
            self.dealer_bg_id = self.canvas.create_image(canvas_width - 600, 0, image=self.background, anchor="nw")
        else:
            self.canvas.itemconfig(self.dealer_bg_id, image=self.background)

        # 🟥 하트 이미지는 표시하지 않음 (원하면 주석 해제)
        # if self.player_heart_id is None:
        #     self.player_heart_id = self.canvas.create_image(50, 50, image=self.hearts[self.player_hp - 1], anchor="nw")
        # else:
        #     self.canvas.itemconfig(self.player_heart_id, image=self.hearts[self.player_hp - 1])

        # if self.dealer_heart_id is None:
        #     self.dealer_heart_id = self.canvas.create_image(canvas_width - 550, 50, image=self.hearts[self.dealer_hp - 1], anchor="nw")
        # else:
        #     self.canvas.itemconfig(self.dealer_heart_id, image=self.hearts[self.dealer_hp - 1])

    def update_hp(self, who, hp):
        hp = max(1, min(6, hp))
        if who == "player":
            self.player_hp = hp
            if self.player_heart_id:
                self.canvas.itemconfig(self.player_heart_id, image=self.hearts[hp - 1])
        elif who == "dealer":
            self.dealer_hp = hp
            if self.dealer_heart_id:
                self.canvas.itemconfig(self.dealer_heart_id, image=self.hearts[hp - 1])

    def shake_heart(self, who):
        target_id = self.player_heart_id if who == "player" else self.dealer_heart_id

        def animate():
            for dx in [-10, 10, -10, 10, 0]:
                if target_id:
                    self.canvas.move(target_id, dx, 0)
                    time.sleep(0.05)

        threading.Thread(target=animate).start()

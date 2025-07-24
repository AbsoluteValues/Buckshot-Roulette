import random
from tkinter import*
from tkinter import messagebox
from PIL import Image, ImageTk

class Game :
    def __init__(self, mode) :
        self.round = 0 # 라운드
        self.mode = mode # 게임 모드
        self.player = None
        self.dealer = None
    
    def startRound(self, playerHealth, dealerHealth) :
        self.round += 1
        print("라운드 ", self.round)

        self.player = Person(self, playerHealth)
        self.dealer = Person(self, dealerHealth)

        while self.player.currentHealth > 0 and self.dealer.currentHealth > 0 :
            if self.mode == "기본" :
                if self.round == 2 :
                    self.player.addItem(2)
                    self.dealer.addItem(2)
                elif self.round == 3 :
                    self.player.addItem(4)
                    self.dealer.addItem(4)
            else :
                amount = random.randrange(1, 5+1)
                self.player.addItem(amount)
                amount = random.randrange(1, 5+1)
                self.dealer.addItem(amount)

            bulletTable = BulletTable()
            bulletTable.generate()
            print("장전될 총알 ", bulletTable.bullets)

            shotgun = Shotgun()
            shotgun.load(bulletTable.bullets)
            print("랜덤으로 장전됨")

            turn = "player"

            while self.player.currentHealth > 0 and self.dealer.currentHealth > 0 and shotgun.bullets :
                if turn == "player" :
                    if self.player.detain:
                        print("수갑에 묶여 턴을 넘깁니다.")
                        self.player.detain = False
                        turn = "dealer"
                        continue

                    if self.mode == "기본" and self.round != 1 :
                        while True :
                            use = input("아이템을 사용하시겠습니까? (y/n): ").strip().lower()
                            if use == 'y':
                                context = {"shotgun": shotgun, "target": self.dealer}
                                useItem(self.player, context)
                            else :
                                break

                    choice = input("쏠 사람을 선택하시오 (you/dealer): ").strip()

                    if choice == "you" :
                        target = self.player
                    else :
                        target = self.dealer
                    
                    result = shotgun.fire(target)

                    print("플레이어 ", self.player.currentHealth)
                    print("딜러 ", self.dealer.currentHealth)

                    if (target == self.dealer) or (target == self.player and result == "실탄") :
                        turn = "dealer"
                else :
                    print("딜러의 선택 : ", end = "")
                    
                    if len(shotgun.bullets) == 1 :
                        if shotgun.bullets[0] == "실탄" :
                            print("player")
                            target = self.player
                        else :
                            print("dealer")
                            target = self.dealer
                    else :
                        target = random.choice([self.dealer, self.player])
                        if target == self.dealer :
                            print("dealer")
                        else :
                            print("player")
                    
                    result = shotgun.fire(target)

                    print("플레이어 ", self.player.currentHealth)
                    print("딜러 ", self.dealer.currentHealth)

                    if (target == self.player) or (target == self.dealer and result == "실탄") :
                        turn = "player"

class Person :
    def __init__(self, game : Game, health) :
        self.game = game
        self.maxHealth = health # 최대 체력
        self.currentHealth = health # 현재 체력
        self.items = [] # 가지고 있는 아이템
        self.detain = False # 스턴 여부
        self.aed = True # 재새동기 여부

    def addHealth(self, amount) :
        if self.currentHealth <= 2 :
            pass
        elif self.currentHealth + amount > self.maxHealth :
            self.currentHealth = self.maxHealth
        else :
            self.currentHealth += amount

    def minusHealth(self, amount) :
        # 기본 모드에서 3라운드 일 때 생명이 2 이하면 aed 사용 불능
        if self.game.mode == "기본" :
            if self.game.round == 3 :
                if self.aed == True and self.currentHealth - amount <= 2 :
                    self.currentHealth -= amount
                    self.aed = False
                elif self.aed == False :
                    self.currentHealth = 0
                else :
                    self.currentHealth -= amount
            else :
                self.currentHealth -= amount
        else :
            if self.aed == True and self.currentHealth - amount <= 2 :
                self.currentHealth -= amount
                self.aed = False
            elif self.aed == False :
                self.currentHealth = 0
            else :
                self.currentHealth -= amount

    def addItem(self, amount):
        item_classes = [
            HandCuffs, Beer, MagnifyingGlass, Cigarret, ChainsawTino, Phone, Inverter, Adrenaline, Drug
        ]
        if self.game.mode == "기본":
            item_classes = item_classes[:5]

        for _ in range(amount):
            self.items.append(random.choice(item_classes)())

class BulletTable() :
    def __init__(self) :
        self.bullets = [] # 총알
        self.live = 0 # 실탄
        self.blank = 0 # 공포

    def reset(self) :
        self.bullets.clear()
        self.live = 0
        self.blank = 0

    # 실탄이 최소 1개여야 함
    # 총알 갯수가 짝수면 실탄과 공탄 갯수 동일
    # 총알 갯수가 홀수면 실탄이나 공탄이 한 개 더 많음
    def generate(self) :
        self.reset()

        amount = random.randrange(2, 8+1)

        if amount % 2 == 0 :
            # 짝수면 공탄 갯수 = 실탄 갯수
            self.live = amount // 2
            self.blank = amount // 2
        else :
            # 홀수면 실탄이나 공탄이 한 개 더 많음
            if random.choice([True, False]) :
                self.live = (amount // 2) + 1
                self.blank = amount // 2
            else :
                self.live = amount // 2
                self.blank = (amount // 2) + 1

        self.bullets = ["실탄"] * self.live + ["공포탄"] * self.blank
        random.shuffle(self.bullets)

class Shotgun() :
    def __init__(self) :
        self.bullets = [] # 총알
        self.damage = 1
        self.sawed = False

    def load(self, bullets) :
        self.bullets = bullets[:]
        random.shuffle(self.bullets)

    def pump(self) :
        return self.bullets.pop(0)

    def fire(self, target) :
        bullet = self.pump()

        if self.sawed == True :
            self.damage = 2
        else :
            self.damage = 1

        if bullet == "실탄" :
            print("탕!")
            target.minusHealth(self.damage)
            self.damage = 1
        else :
            print("틱!")
            self.damage = 1
        
        return bullet

class Item:
    def __init__(self, name = "아이템"):
        self.name = name

    def use(self, user, target = None, context = None):
        raise NotImplementedError()

    def __str__(self):
        return self.name

def useItem(player, context):
    if not player.items :
        print("사용 가능한 아이템이 없습니다.")
        return

    print("사용할 아이템을 선택하세요:")
    for i, item in enumerate(player.items) :
        print(f"{i + 1}. {item}")

    idx = int(input("번호 입력: ")) - 1
    if 0 <= idx < len(player.items) :
        name = player.items[idx].name

        item_classes = {
            "수갑": HandCuffs(),
            "맥주": Beer(),
            "돋보기": MagnifyingGlass(),
            "담배": Cigarret(),
            "톱": ChainsawTino(),
            "대포폰": Phone(),
            "변환기": Inverter(),
            "아드레날린": Adrenaline(),
            "상한 약": Drug()
        }
        item = item_classes.get(name)
        if item :
            item.use(player, game.dealer if name == "수갑" else None, context)
            del player.items[idx]

# 수갑 : 상대 턴 제약
class HandCuffs(Item) :
    def __init__(self) :
        super().__init__("수갑")

    def use(self, user, target, context = None) :
        target.detain = True

# 맥주 : 현재 장전된 탄약 배출
class Beer(Item) :
    def __init__(self) :
        super().__init__("맥주")

    def use(self, user, target = None, context = None) :
        shotgun = context.get("shotgun") if context else None
        removed = shotgun.pump()
        print(f"'{removed}' 탄약 배출됨")

# 돋보기 : 현재 장전된 탄약 확인
class MagnifyingGlass(Item) :
    def __init__(self) :
        super().__init__("돋보기")

    def use(self, user, target = None, context = None) :
        shotgun = context.get("shotgun") if context else None
        if shotgun.bullets :
            print(f"'{shotgun.bullets[0]}'입니다.")

class Cigarret(Item) :              # 담배 : 체력 1 회복
    def __init__(self) :
        super().__init__("담배")
    def use(self, user, target = None, context = None) :
        before = user.currentHealth
        user.addHealth(1)
        print(f"체력 {before} -> {user.currentHealth}")

class ChainsawTino(Item) :          # 톱 : 탄환의 공격력 2배증가
    def __init__(self) :
        super().__init__("포티노")
    def use(self, user, target = None, context = None) :
        user.doubleDamage = True
        print(f"{user}'s damage is double")

class Phone(Item) :                 # 대포폰 : 장전된 탄환 외 나머지 탄환중 랜덤으로 몇번째탄약이 실탄인지 공포탄인지 알려줌
    def __init__(self) :
        super().__init__("대포폰")
    def use(self, user, target = None, context = None) :
        shotgun = context.get("shotgun") if context else None
        if shotgun and len(shotgun.bullets) > 1 :
            remaining = shotgun.bullets[1:]
            idx = random.randrange(len(remaining))
            print(f"{idx + 2}번째 탄은 '{remaining[idx]}")
            
class Inverter(Item) :              # 변환기 : 현재 장전된 탄약을 전환 (실탄 <-> 공포탄)
    def __init__(self) :
        super().__init__("변환기")
    def use(self, user, target = None, context = None) :
        shotgun = context.get("shotgun") if context else None
        if shotgun and shotgun.bullets :
            before = shotgun.bullets[0]
            shotgun.bullets[0] = "공포탄" if before == "실탄" else "실탄"
            
class Adrenaline(Item) :            # 아드레날린 : 상대의 아이템 한개를 강탈
    def __init__(self) :
        super().__init__("아드레날린")
    def use(self, user, target, context = None) :
        if not target.items :       # GUI 구현 후 메세지박스를 이용해 "상대방이 아이템을 보유하지 않음 출력"
            return
        def onSelect(index) :
            stolen = target.items.pop(index)
            user.items.append(stolen)
            messagebox.showinfo("강탈 : ",f"{stolen.name}")
            
        #GUI구현 후 제작

class Drug(Item) :                  # 약 : 50%의 확률로 회복 or 체력 -1
    def __init__(self) :
        super().__init__("상한 약")
    def use(self, user, target = None, context = None) :
        if random.choice([True, False]) :
            user.addHealth(1)
        else :
            user.minusHealth(1)

# select = input("게임 모드를 선택하시오(기본/무한) : ")

game = Game("기본")

game.startRound(2, 2)


###############################################################################################################################


def Click(event):
    userbox_x, userbox_y = 645, 550

    # 이미지 크기 가져오기 (실제 이미지 크기를 사용)
    bbox = canvas.bbox("userBox")  # userBox 태그가 붙은 이미지 영역 반환 (x1,y1,x2,y2)
    if bbox:
        x1, y1, x2, y2 = bbox
        # 클릭 위치가 아이템 박스 이미지 영역 내인지 체크
        if x1 <= event.x <= x2 and y1 <= event.y <= y2 :
            pass
        else:
            print(f"클릭 위치: x={event.x}, y={event.y} (아이템 박스 아님)")
    else:
        print("userBox 이미지 영역을 찾을 수 없습니다.")

# 인벤토리 슬롯 좌표 (왼쪽 인벤토리 2x2 기준)
inventory_slots = [
    (265, 457),
    (419, 450),
    (259, 566),
    (420, 564)
]

# 윈도우 초기화
window = Tk()
window.title("Buckshot Roulette")
window.geometry("1280x720")
window.iconbitmap("./image/Buckshot_Roulette.ico")

canvas = Canvas(window, width=1280, height=720, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# 배경 이미지
wall_photo = ImageTk.PhotoImage(Image.open("./image/wallpaper.png").convert("RGBA").resize((1280, 720)))
canvas.create_image(0, 0, image=wall_photo, anchor="nw")

# 게임 보드
board_photo = ImageTk.PhotoImage(Image.open("./image/game_board.png").convert("RGBA").resize((1280, 720)))
canvas.create_image(0, 0, image=board_photo, anchor="nw")

# 아이템 지급 이미지 참조 유지
loaded_item_images = []

# 아이템 캔버스 객체 태그 저장
selectedCanvasItems = []

# 아이템 지급 함수


# 전체 창 클릭 시 좌표 확인 및 아이템 박스 클릭 여부 체크
window.bind("<Button-1>", Click)

window.mainloop()

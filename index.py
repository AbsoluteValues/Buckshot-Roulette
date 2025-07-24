import random
from tkinter import messagebox

class Game :
    def __init__(self, mode) :
        self.round = 0 # 라운드
        self.mode = mode # 게임 모드
    
    def startRound(self, playerHealth, dealerHealth) :
        self.round += 1
        print("라운드 ", self.round)

        player = Person(self, playerHealth)
        dealer = Person(self, dealerHealth)

        while player.currentHealth > 0 and dealer.currentHealth > 0 :
            bulletTable = BulletTable()
            bulletTable.generate()
            print("장전될 총알 ", bulletTable.bullets)

            shotgun = Shotgun()
            shotgun.load(bulletTable.bullets)
            print("랜덤으로 장전됨")

            turn = "player"

            while player.currentHealth > 0 and dealer.currentHealth > 0 and shotgun.bullets :
                if turn == "player" :
                    choice = input("쏠 사람을 선택하시오 (you/dealer): ")
                    if choice == "you" :
                        result = shotgun.fire(player)
                        if result == "실탄" :
                            turn = "dealer"
                        print("플레이어 ", player.currentHealth)
                        print("딜러 ", dealer.currentHealth)
                    else :
                        result = shotgun.fire(dealer)
                        turn = "dealer"
                        print("플레이어 ", player.currentHealth)
                        print("딜러 ", dealer.currentHealth)
                else :
                    print("<딜러> : ", end = "")
                    if random.choice([True, False]) :
                        print("dealer")
                        result = shotgun.fire(dealer)
                        if result == "실탄" :
                            turn = "player"
                        print("플레이어 ", player.currentHealth)
                        print("딜러 ", dealer.currentHealth)
                    else :
                        print("you")
                        result = shotgun.fire(player)
                        turn = "player"
                        print("플레이어 ", player.currentHealth)
                        print("딜러 ", dealer.currentHealth)

class Person() :
    def __init__(self, game : Game, health) :
        self.game = game
        self.maxHealth = health # 최대 체력
        self.currentHealth = health # 현재 체력
        self.items = [] # 가지고 있는 아이템
        self.detain = False # 스턴 여부
        self.aed = True # 재새동기 여부

    def addHealth(self, health) :
        if self.currentHealth + health > self.maxHealth :
            self.currentHealth = self.maxHealth
        else :
            self.currentHealth += health

    def minusHealth(self, health) :
        if self.aed == True :
            self.currentHealth -= health

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

    def load(self, bullets) :
        self.bullets = bullets[:]
        random.shuffle(self.bullets)

    def pump(self) :
        if self.bullets[0] == "실탄" :
            self.bullets.pop(0)
            return "실탄"
        else :
            self.bullets.pop(0)
            return "공포탄"

    def fire(self, target, damage) :
        if self.bullets[0] == "실탄" :
            target.minusHealth(damage)
        self.pump()

class Item :                  # 상위클래스
    def __init__(self, name = "아이템") :
        self.name = name
    def use(self, user, target = None, context = None) :
        raise NotImplementedError()

class HandCuffs(Item) :             # 수갑 : 상대 턴 제약
    def __init__(slef) :
        super().__init__("수갑")
    def use(self, user, target, cntext = None) :
        if target :
            target.detain = True
            print(f"{target}은/는 다음턴 압수")

class Beer(Item) :                  # 맥주 : 현재 장전된 탄약 배출
    def __init__(self) :
        super().__init__("맥주")
    def use(self, user, target = None, context = None) :
        shotgun = context.get("shotgun") if context else None
        remove = shotgun.bullets.pop(0)
        print(f"'{remove}'탄약 배출")

class MagnifyingGlass(Item) :       # 돋보기 : 현재 장전된 탄약 확인
    def __init__(self) :
        super().__init__("돋보기")
    def use(self, user, target = None, context = None) :
        shotgun = context.get("shotgun") if context else None
        if shotgun and shotgun.bullets :
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

game = Game("기본")
game.nextRound()

player = Person(2)
dealer = Person(2)

bulletTable = BulletTable()
bulletTable.generate()
print("테이블 ", bulletTable.bullets)

shotgun = Shotgun()
shotgun.load(bulletTable.bullets)
print("샷건 ", shotgun.bullets)

for _ in range(len(shotgun.bullets)) :
    shotgun.fire(player, 1)

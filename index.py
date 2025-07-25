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
        print(f"\n[라운드 {self.round}]")

        self.player = Person(self, playerHealth)
        self.dealer = Person(self, dealerHealth)

        # 1회 장전
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

            print("<플레이어의 아이템>")
            for i, item in enumerate(self.player.items) :
                print(item)

            print("<딜러의 아이템>")
            for i, item in enumerate(self.dealer.items) :
                print(item)

            bulletTable = BulletTable()
            bulletTable.generate()
            print("장전될 총알 ", bulletTable.bullets)

            shotgun = Shotgun()
            shotgun.load(bulletTable.bullets)
            print("랜덤으로 장전됨")

            self.player.detain = False
            self.dealer.detain = False

            turn = "player"

            # 장전 사이클
            while self.player.currentHealth > 0 and self.dealer.currentHealth > 0 and shotgun.bullets :
                if turn == "player" :
                    if self.player.detain:
                        print("수갑에 묶여 플레이어가 턴을 넘깁니다.")
                        self.player.detain = False
                        turn = "dealer"
                        continue

                    if self.mode == "기본" and self.round != 1 :
                        while True :
                            use = input("아이템을 사용하시겠습니까? (y/n): ").strip().lower()
                            if use == 'y':
                                useItem(self.player, self.dealer, shotgun)
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
                    if self.dealer.detain :
                        print("수갑에 묶여 딜러가 턴을 넘깁니다.")
                        self.dealer.detain = False
                        turn = "player"
                        continue

                    if self.mode == "기본" and self.round != 1 :
                        self.dealerUseItem(self.dealer, self.player, shotgun)

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
        self.handcuffCooldown = 0  # 수갑 쿨타임
        self.aed = True # 재새동기 여부(회생)

    def addHealth(self, amount) :
        if self.game.mode == "기본" and self.game.round == 3 and self.currentHealth <= 2 :
            pass
        elif self.game.mode == "무한" and self.currentHealth <= 2 :
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

    def addItem(self, amount) :
        item_classes = [
            HandCuffs, Beer, MagnifyingGlass, Cigarret, ChainsawTino, Phone, Inverter, Adrenaline, Drug
        ]
        if self.game.mode == "기본":
            item_classes = item_classes[:5]

        for _ in range(amount):
            self.items.append(random.choice(item_classes)())

    def dealerUseItem(self, target, shotgun) :
        if not self.items or not shotgun.bullets :
            return

        current_bullet = shotgun.bullets[0]
        used_indices = set()

        # 오래된 순서대로, 같은 시기에 들어온 아이템은 랜덤하게 섞어서 순서 결정
        sorted_items = self.items[:]
        random.shuffle(sorted_items)
        for i, item in enumerate(sorted_items) :
            name = item.name

            if i in used_indices:
                continue

            # 1. 수갑: 항상 사용
            if name == "수갑" and not target.detain :
                item.use(self, target, shotgun)
                print("딜러가 '수갑'을 사용했습니다.")
                self.items.remove(item)
                continue

            # 2. 돋보기: 총알이 무엇인지 모를 경우에만 사용
            if name == "돋보기" :
                if current_bullet not in ["실탄", "공포탄"] :
                    item.use(self, None, shotgun)
                    print("딜러가 '돋보기'로 총알을 확인했습니다.")
                    current_bullet = shotgun.bullets[0]
                    self.items.remove(item)
                    continue

            # 3. 맥주: 현재 탄이 위험할 수 있고, 최소 2발 이상 있을 때
            if name == "맥주" :
                if len(shotgun.bullets) >= 2 :
                    item.use(self, None, shotgun)
                    print("딜러가 '맥주'로 탄을 배출했습니다.")
                    current_bullet = shotgun.bullets[0] if shotgun.bullets else None
                    self.items.remove(item)
                    continue

            # 4. 담배: 체력이 감소해 있으면 사용
            if name == "담배" :
                if self.currentHealth < self.maxHealth :
                    item.use(self, None, shotgun)
                    print("딜러가 '담배'를 사용했습니다.")
                    self.items.remove(item)
                    continue

            # 5. 톱: 총알이 1발만 남았고, 그것이 실탄이거나 그럴 가능성이 높을 경우
            if name == "톱" :
                if len(shotgun.bullets) == 1 and current_bullet == "실탄" :
                    item.use(self, None, shotgun)
                    print("딜러가 '톱'을 사용했습니다.")
                    self.items.remove(item)
                    continue

            # 6. 대포폰: 남은 탄이 많을수록 가치가 있음
            if name == "대포폰" :
                if len(shotgun.bullets) >= 3 :
                    item.use(self, None, shotgun)
                    print("딜러가 '대포폰'을 사용했습니다.")
                    self.items.remove(item)
                    continue

            # 7. 변환기: 현재 탄이 실탄이면 공포탄으로 바꾸기
            if name == "변환기" :
                if current_bullet == "실탄" :
                    item.use(self, None, shotgun)
                    print("딜러가 '변환기'로 실탄을 공포탄으로 전환했습니다.")
                    current_bullet = shotgun.bullets[0]
                    self.items.remove(item)
                    continue

            # 8. 아드레날린: 플레이어가 아이템을 가지고 있을 때만
            if name == "아드레날린" :
                if target.items:
                    item.use(self, target, shotgun)
                    print("딜러가 '아드레날린'으로 아이템을 강탈했습니다.")
                    self.items.remove(item)
                    continue

            # 9. 상한 약: 체력 부족 시 사용 (50% 회복)
            if name == "약" :
                if self.currentHealth < self.maxHealth :
                    item.use(self, None, shotgun)
                    print("딜러가 '약'을 복용했습니다.")
                    self.items.remove(item)
                    continue

    def turnStart(self):
        if self.handcuffCooldown > 0:
            self.handcuffCooldown -= 1

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
        else :
            print("틱!")

        self.sawed = False

        return bullet

class Item:
    def __init__(self, name = "아이템"):
        self.name = name

    def use(self, user, target = None, shotgun = None):
        raise NotImplementedError()

    def __str__(self):
        return self.name

def useItem(player, dealer, shotgun) :
    if not player.items :
        print("사용 가능한 아이템이 없습니다.")
        return

    print("사용할 아이템을 선택하세요:")
    for i, item in enumerate(player.items) :
        print(f"{i + 1}. {item}")
    print("0. 뒤로가기")

    idx = int(input("번호 입력: ")) - 1
    if 0 <= idx < len(player.items) :
        name = player.items[idx].name

        item_classes = {
            "수갑": HandCuffs,
            "맥주": Beer,
            "돋보기": MagnifyingGlass,
            "담배": Cigarret,
            "톱": ChainsawTino,
            "대포폰": Phone,
            "변환기": Inverter,
            "아드레날린": Adrenaline,
            "상한 약": Drug
        }
        item = item_classes.get(name)
        if item :
            item().use(player, dealer, shotgun)
            del player.items[idx]

# 수갑 : 상대 턴 제약(한 턴의 쿨타임)
class HandCuffs(Item) :
    def __init__(self) :
        super().__init__("수갑")

    def use(self, user, target, shotgun) :
        if user.handcuffCooldown == 0:
            target.detain = True
            user.handcuffCooldown = 2  # 2턴 쿨타임 예시
        else:
            print("수갑은 아직 사용 불가합니다.")

# 맥주 : 현재 장전된 탄약 배출
class Beer(Item) :
    def __init__(self) :
        super().__init__("맥주")

    def use(self, user, target = None, shotgun = None) :
        removed = shotgun.pump()
        print(f"'{removed}' 탄약 배출됨")

# 돋보기 : 현재 장전된 탄약 확인
class MagnifyingGlass(Item) :
    def __init__(self) :
        super().__init__("돋보기")

    def use(self, user, target = None, shotgun = None) :
        if shotgun.bullets :
            print(f"'{shotgun.bullets[0]}'입니다.")

# 담배 : 체력 1 회복
class Cigarret(Item) :
    def __init__(self) :
        super().__init__("담배")

    def use(self, user, target = None, shotgun = None) :
        before = user.currentHealth
        user.addHealth(1)
        print(f"체력 {before} -> {user.currentHealth}")

# 톱 : 탄환의 공격력 2배증가
class ChainsawTino(Item) :
    def __init__(self) :
        super().__init__("톱")

    def use(self, user, target = None, shotgun = None) :
        shotgun.sawed = True

# 대포폰 : 장전된 탄환 외 나머지 탄환중 랜덤으로 몇번째탄약이 실탄인지 공포탄인지 알려줌
class Phone(Item) :
    def __init__(self) :
        super().__init__("대포폰")

    def use(self, user, target = None, shotgun = None) :
        if len(shotgun.bullets) > 1 :
            remaining = shotgun.bullets[1:]
            idx = random.randrange(len(remaining))
            print(f"{idx + 2}번째 탄은 '{remaining[idx]}'입니다")

# 변환기 : 현재 장전된 탄약을 전환 (실탄 <-> 공포탄)
class Inverter(Item) :
    def __init__(self) :
        super().__init__("변환기")

    def use(self, user, target = None, shotgun = None) :
        if shotgun.bullets[0] == "실탄" :
            shotgun.bullets[0] = "공포탄"
        else :
            shotgun.bullets[0] = "실탄"

# 아드레날린 : 상대의 아이템 한개를 강탈
class Adrenaline(Item) :      
    def __init__(self) :
        super().__init__("아드레날린")

    def use(self, user, target, shotgun = None) :
        if not target.items :
            pass
        def onSelect(index) :
            stolen = target.items.pop(index)
            user.items.append(stolen)
            messagebox.showinfo("강탈 : ",f"{stolen.name}")

# 약 : 50%의 확률로 회복 or 체력 -1
class Drug(Item) :
    def __init__(self) :
        super().__init__("약")

    def use(self, user, target = None, shotgun = None) :
        if random.choice([True, False]) :
            user.addHealth(1)
        else :
            user.minusHealth(1)



# select = input("게임 모드를 선택하시오(기본/무한) : ")

game = Game("기본")

health = [2, 4, 6]

i = 0
while i < 3 :
    game.startRound(health[i], health[i])
    if game.mode == "기본" and game.player.currentHealth == 0 and game.round != 3 :
        print("<의사 : 넌 아직 죽기에는 일러!>")
        game.round -= 1
        continue
    i += 1

import random
from tkinter import*
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

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
                    print("\n<내 턴>")
                    self.player.turnStart()

                    if self.player.detain:
                        print("수갑에 묶여 플레이어가 턴을 넘깁니다.")
                        self.player.detain = False
                        turn = "dealer"
                        continue

                    if shotgun.bullets :
                        if self.mode == "무한" or (self.mode == "기본" and self.round != 1) :
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
                    print("\n<딜러 턴>")
                    self.dealer.turnStart()

                    if self.dealer.detain :
                        print("수갑에 묶여 딜러가 턴을 넘깁니다.")
                        self.dealer.detain = False
                        turn = "player"
                        continue
                    
                    if shotgun.bullets :
                        currentBullet = ""
                        if self.mode == "무한" or (self.mode == "기본" and self.round != 1) :
                            currentBullet = self.dealer.dealerUseItem(self.player, shotgun)

                        print("딜러의 선택 : ", end = "")
                        
                        if len(shotgun.bullets) == 1 or currentBullet != "" :
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
            self.currentHealth -= amount
            if self.currentHealth < 0 :
                self.currentHealth = 0

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

        currentBullet = ""

        # 오래된 순서대로, 같은 시기에 들어온 아이템은 랜덤하게 섞어서 순서 결정
        sorted_items = self.items[:]
        random.shuffle(sorted_items)
        for i, item in enumerate(sorted_items) :
            name = item.name

            # 1. 수갑: 항상 사용
            if name == "수갑" and not target.detain :
                item.use(self, target, shotgun)
                print("딜러가 '수갑'을 사용했습니다.")
                self.items.remove(item)
                continue

            # 2. 돋보기: 총알이 무엇인지 모를 경우에만 사용
            if name == "돋보기" :
                if not currentBullet :
                    item.use(self, None, shotgun)
                    print("딜러가 '돋보기'로 총알을 확인했습니다.")
                    currentBullet = shotgun.bullets[0]
                    self.items.remove(item)
                    continue

            # 3. 맥주: 현재 탄이 위험할 수 있고, 최소 2발 이상 있을 때
            if name == "맥주" :
                if len(shotgun.bullets) >= 2 :
                    item.use(self, None, shotgun)
                    print("딜러가 '맥주'로 탄을 배출했습니다.")
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
                if len(shotgun.bullets) == 1 and currentBullet == "실탄" :
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
                if currentBullet == "실탄" :
                    item.use(self, None, shotgun)
                    print("딜러가 '변환기'로 실탄을 공포탄으로 전환했습니다.")
                    currentBullet = shotgun.bullets[0]
                    self.items.remove(item)
                    continue

            # 8. 아드레날린: 플레이어가 아이템을 가지고 있을 때만
            if name == "아드레날린" :
                candidates = [item for item in target.items if item.name != "아드레날린"]
                if not candidates :
                    print("딜러: 강탈할 수 있는 아이템이 없습니다.")
                    continue

                # 평가 함수: 아이템별 전략적 스코어링
                def evaluate_item_score(item):
                    score = 0

                    # 회복 방해: 플레이어 체력 낮음
                    if target.currentHealth <= 2 and item.name in ["담배", "상한 약"]:
                        score += 100

                    # 딜러 체력 낮음: 회복용 확보
                    if self.currentHealth < self.maxHealth and item.name in ["담배", "상한 약"]:
                        score += 80

                    # 탄환 1개: 공격 아이템 중요
                    if len(shotgun.bullets) == 1 and item.name in ["톱", "맥주"]:
                        score += 90

                    # 탄환 여유 있음: 정보 계열 확보
                    if len(shotgun.bullets) >= 3 and item.name in ["돋보기", "변환기", "대포폰"]:
                        score += 70

                    # 상대 아이템 많을 때 방해
                    if len(target.items) >= 3 and item.name in ["수갑", "변환기", "톱"]:
                        score += 60

                    # 수갑은 항상 유용하지만 쿨타임 고려
                    if item.name == "수갑":
                        if self.handcuffCooldown == 0:
                            score += 50
                        else:
                            score -= 100

                    # 기본 우선순위 점수
                    base_priority = {
                        "톱": 50,
                        "변환기": 45,
                        "맥주": 40,
                        "돋보기": 35,
                        "대포폰": 30,
                        "수갑": 25,
                        "상한 약": 20,
                        "담배": 15,
                    }
                    score += base_priority.get(item.name, 0)

                    return score

                # 점수 기반 정렬
                scored_items = sorted(candidates, key=lambda item: evaluate_item_score(item), reverse=True)
                stolen = scored_items[0]
                target.items.remove(stolen)
                print(f"딜러가 아드레날린으로 '{stolen.name}'을(를) 강탈했습니다.")

                if stolen.name in ["톱", "맥주", "돋보기", "변환기", "대포폰", "상한 약", "담배"] :
                    stolen.use(self, None, shotgun)
                    print(f"딜러가 '{stolen.name}'을 사용했습니다.")
                elif stolen.name == "수갑" :
                    if not target.detain and self.handcuffCooldown == 0 :
                        stolen.use(self, target, shotgun)
                        print("딜러가 '수갑'을 사용했습니다.")

                self.items.remove(item)
                continue

            # 9. 상한 약: 체력 부족 시 사용 (50% 회복)
            if name == "상한 약" :
                if self.currentHealth < self.maxHealth :
                    item.use(self, None, shotgun)
                    print("딜러가 '상한 약'을 복용했습니다.")
                    self.items.remove(item)
                    continue

        return currentBullet

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

class Item :
    def __init__(self, name = "아이템") :
        self.name = name

    def use(self, user, target = None, shotgun = None) :
        raise NotImplementedError()

    def __str__(self) :
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
            user.handcuffCooldown = 2
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

# 대포폰 : 장전된 탄환 외 나머지 탄환중 랜덤으로 
# 몇번째탄약이 실탄인지 공포탄인지 알려줌
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

    def use(self, user, target, shotgun=None) :
        # 아드레날린 제외
        candidates = [item for item in target.items if item.name != "아드레날린"]

        if not candidates :
            print("상대방에게 강탈 가능한 아이템이 없습니다.")
            return

        print("강탈 가능한 상대방의 아이템 목록:")
        for i, item in enumerate(candidates) :
            print(f"{i + 1}. {item}")

        while True :
            try :
                idx = int(input("강탈할 아이템 번호를 선택하세요: ")) - 1
                if 0 <= idx < len(candidates) :
                    stolen = candidates[idx]
                    target.items.remove(stolen)
                    print(f"'{stolen.name}' 아이템을 강탈했습니다.")
                    self.attempt_use(stolen, user, target, shotgun)
                    break
                else:
                    print("올바른 번호를 입력하세요.")
            except ValueError :
                print("숫자를 입력하세요.")

    def attempt_use(self, item, user, target, shotgun) :
        if item.name in ["톱", "맥주", "돋보기", "변환기", "대포폰", "상한 약", "담배"] :
            item.use(user, None, shotgun)
            print(f"'{item.name}'을(를) 사용했습니다.")
        elif item.name == "수갑" :
            if not target.detain and user.handcuffCooldown == 0 :
                item.use(user, target, shotgun)
                print("'수갑'을 사용했습니다.")
            else :
                print("수갑은 현재 사용할 수 없습니다.")

# 상한 약 : 50%의 확률로 회복 or 체력 -1
class Drug(Item) :
    def __init__(self) :
        super().__init__("상한 약")

    def use(self, user, target = None, shotgun = None) :
        before = user.currentHealth
        if random.choice([True, False]) :
            user.addHealth(1)
        else :
            user.minusHealth(1)
        print(f"체력 {before} -> {user.currentHealth}")

conn = pymysql.connect(host = 'localhost', port = 3306, user = 'root', password = '1234', db = 'buckshot_roulette', charset = 'utf8')
cursor = conn.cursor()

nickname = input("닉네임을 입력하시오 : ")

sql = 'SELECT * FROM player WHERE nickname = %s'
vals = (nickname)
cursor.execute(sql, vals)

row = cursor.fetchone()
if row is None:
    print('검색 결과 없음')
    sql = "INSERT INTO player VALUES(%s, %d, %d)"
    vals = (nickname, 0)
    cursor.execute(sql, vals)
    conn.commit()
else:
    print(row)

select = input("게임 모드를 선택하시오(기본/무한) : ")

game = Game(select)

if game.mode == "무한" :
    while True :
        hp = random.randint(2, 4+1)
        game.startRound(hp, hp)
        if game.player.currentHealth == 0 :
            sql = "UPDATE student SET death = %d WHERE nickname = %s"
            vals = (1, nickname)
            cursor.execute(sql, vals)
            conn.commit()
            print("플레이어 사망. 게임 오버.")
            break
        elif game.dealer.currentHealth == 0 :
            sql = "UPDATE student SET win = %d WHERE nickname = %s"
            vals = (1, nickname)
            cursor.execute(sql, vals)
            conn.commit()
            print("딜러 사망. 계속 진행됩니다.")
else :
    health = [2, 4, 6]
    i = 0
    while i < 3 :
        game.startRound(health[i], health[i])
        if game.player.currentHealth == 0 and game.round != 3 :
            print("<의사 : 넌 아직 죽기에는 일러!>")
            sql = "UPDATE student SET death = %d WHERE nickname = %s"
            vals = (1, nickname)
            cursor.execute(sql, vals)
            conn.commit()
            game.round -= 1
            continue
        i += 1
        sql = "UPDATE student SET win = %d WHERE nickname = %s"
        vals = (1, nickname)
        cursor.execute(sql, vals)
        conn.commit()
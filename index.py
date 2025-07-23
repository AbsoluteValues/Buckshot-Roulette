import random

class Game :
    def __init__(self, mode) :
        self.round = 0 # 라운드
        self.mode = mode # 게임 모드
    
    def nextRound(self) :
        self.round += 1

class Person() :
    def __init__(self, health) :
        self.maxHealth = health # 최대 체력
        self.currentHealth = self.maxHealth # 현재 체력
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

class HandCuffs:             # 수갑 : 상대 턴 제약
    print("수갑")

class Beer:                  # 맥주 : 현재 장전된 탄약 배출
    print("맥주")

class MagnifyingGlass:       # 돋보기 : 현재 장전된 탄약 확인
    print("돋보기")

class Cigarret:              # 담배 : 체력 1 회복
    print("담배")

class ChainsawTino:          # 톱 : 탄환의 공격력 2배증가
    print("톱")

class Phone:                 # 대포폰 : 장전된 탄환 외 나머지 탄환중 랜덤으로 몇번째탄약이 실탄인지 알려줌
    print("폰")

class Inverter:              # 변환기 : 현재 장전된 탄약을 전환 (실탄 <-> 공포탄)
    print("변환기")

class Adrenaline:            # 아드레날린 : 상대의 아이템 한개를 강탈
    print("아드레날린")

class Drug:                  # 약 : 50%의 확률로 회복 or 체력 -1
    print("약")

bulletTable = BulletTable()
bulletTable.generate()
print("테이블 ", bulletTable.bullets)

shotgun = Shotgun()
shotgun.load(bulletTable.bullets)
print("샷건 ", shotgun.bullets)

for _ in range(len(shotgun.bullets)) :
    shotgun.fire()
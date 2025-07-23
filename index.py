import random

class BulletTable() :
    def __init__(self) :
        self.bullets = [] # 총알
        self.live = 0 # 실탄
        self.blank = 0 # 공포

    def reset(self) :
        self.bullets.clear()
        self.live = 0
        self.blank = 0

    def generate(self) :
        self.reset()

        amount = random.randrange(2, 8+1)

        for _ in range(amount) :
            num = random.randrange(0, 1+1)
            if num == 1 :
                self.live += 1
                self.bullets.append("실탄")
            else :
                self.blank += 1
                self.bullets.append("공포탄")

class Shotgun() :
    def __init__(self) :
        self.bullets = [] # 총알

    def load(self, bullets) :
        self.bullets = bullets[:]
        random.shuffle(self.bullets)

    def fire(self) :
        if self.bullets[0] == "실탄" :
            print("실탄")
        else :
            print("공포탄")
        
        self.bullets.pop(0)
        
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
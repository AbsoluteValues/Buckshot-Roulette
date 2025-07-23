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

bulletTable = BulletTable()
bulletTable.generate()
print("테이블 ", bulletTable.bullets)

shotgun = Shotgun()
shotgun.load(bulletTable.bullets)
print("샷건 ", shotgun.bullets)

for _ in range(len(shotgun.bullets)) :
    shotgun.fire()
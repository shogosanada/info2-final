import pyxel
import random

class Pad:
    def __init__(self):
        self.x = 100
        self.y = 195
        self.w = 20
        self.h = 5
        self.c = pyxel.COLOR_PINK
        self.game_over = False
        self.game_clear = False

    def draw(self):
        pyxel.rect(self.x - self.w/2, self.y, self.w, self.h, self.c)

    def update(self, bullets, targets, enemy_bullets):
        if self.game_over or self.game_clear:
            return

        self.x = pyxel.mouse_x
        if pyxel.btnp(pyxel.KEY_SPACE):
            if len(bullets) > 0:
                if bullets[-1].y <= 100:
                    bullets.append(Bullet(self.x, self.y))
            else:
                bullets.append(Bullet(self.x, self.y))

        # Check for collisions with targets
        # for target in targets:
        #     for bullet in bullets:
        #         if self.check_collision(bullet, target):
        #             targets.remove(target)
        #             bullets.remove(bullet)
        #             self.score += 1
        #             if not targets:
        #                 self.game_clear = True
        #             return True  # Indicates a hit

        # Check for collisions with enemy bullets
        for enemy_bullet in enemy_bullets:
            if self.check_collision(enemy_bullet, self):
                self.game_over = True

    def check_collision(self, a, b):
        return (
            a.x < b.x+b.w/2 and
            a.x  > b.x - b.w/2 and
            a.y < b.y + b.h/2 and
            a.y + 2 > b.y-b.h/2
        )

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.s = 2
        self.c = pyxel.COLOR_BLACK

    def draw(self):
        pyxel.rect(self.x, self.y, 2, 2, self.c)

    def move(self):
        self.y -= self.s
        return self.y >= 0

class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.s = 1
        self.c = pyxel.COLOR_YELLOW

    def draw(self):
        pyxel.rect(self.x, self.y, 2, 2, self.c)

    def move(self):
        self.y += self.s
        return self.y <= pyxel.height

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 20
        self.h = 10
        self.speed = 1
        self.direction = 1
        self.c = pyxel.COLOR_RED
        self.shoot_timer = random.randint(30, 60)

    def draw(self,i):
        # pyxel.rect(self.x - self.w/2, self.y, self.w, self.h, self.c)
        pyxel.blt(self.x, self.y,0,(i+1) * 16,0,15,15,0)

    def update(self, enemy_bullets):
        self.x += self.speed * self.direction

        if self.x - self.w/2 <= 0 or self.x + self.w/2 >= pyxel.width:
            self.direction *= -1

        self.shoot_timer -= 1
        if self.shoot_timer == 0:
            enemy_bullets.append(EnemyBullet(self.x, self.y))
            self.shoot_timer = random.randint(30, 60)

class App:
    def __init__(self):
        pyxel.init(200, 200)
        pyxel.load("my_resource.pyxres")
        self.pad = Pad()
        self.bullets = []
        self.targets = []
        self.enemy_bullets = []
        self.score = 0
        self.generate_targets()
        
        pyxel.run(self.update, self.draw)

    def update(self):
        self.pad.update(self.bullets, self.targets, self.enemy_bullets)

        if self.pad.game_over or self.pad.game_clear:
            return

        for i in reversed(range(len(self.bullets))):
            if not self.bullets[i].move():
                del self.bullets[i]

        for target in self.targets:
            target.update(self.enemy_bullets)

        for i in reversed(range(len(self.enemy_bullets))):
            if not self.enemy_bullets[i].move():
                del self.enemy_bullets[i]
        #追加部分（26-34行目を移植し、調整）
        for target in self.targets:
            for bullet in self.bullets:
                if self.pad.check_collision(bullet, target):
                    self.targets.remove(target)
                    self.bullets.remove(bullet)
                    self.score += 1
                    if not self.targets:
                        self.pad.game_clear = True
                    return True  # Indicates a hit

    def draw(self):
        pyxel.cls(7)

        if self.pad.game_over:
            pyxel.text(70, 90, "Game Over", 0)
            pyxel.text(50, 110, f"Score: {self.score}", 0)
            return

        if self.pad.game_clear:
            pyxel.text(70, 90, "Game Clear!", 0)
            pyxel.text(50, 110, f"Score: {self.score}", 0)
            return

        self.pad.draw()

        for bullet in self.bullets:
            bullet.draw()

        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.draw()

        for i, target in enumerate(self.targets):
            target.draw(i%5)

        pyxel.text(10, 10, f"Score: {self.score}", pyxel.COLOR_BLACK)

    def generate_targets(self):
        for i in range(5):
            for j in range (2):
                self.targets.append(Target(i * 40 + 20, j*20 + 10))

        # for i in range(5):
                
        # i = 0
                #j = 0 (20,10)
                #j = 1 (20,30)
        # i = 1
                #j = 0 (60,10)
                #j = 1 (60,30)
        #:
        
        # i = 4
                # j = 0 (180,10)
                # j = 1 (180,30)

App()
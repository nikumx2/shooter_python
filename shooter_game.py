#Проект шутер
from pygame import *
from random import *
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
   
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()


        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
           
        if keys[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x += self.speed
   
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 16, 20, 10)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        # Увеличивать координату у на скорость
        self.rect.y += self.speed


        # Глобальная переменная (счетчик пропущенных)
        global lost


        # Условие при котором:
        # Если враг достиг нижней точки экрана, то переместить его вверх
        # И увеличить счетчик пропущенных на 1
        if self.rect.y > win_height:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(10, win_width - 80)


class Asteroid(GameSprite):
    def update(self):
        # Увеличивать координату у на скорость
        self.rect.y += self.speed


        # Условие при котором:
        # Если враг достиг нижней точки экрана, то переместить его вверх
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(10, win_width - 80)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()




#Подключение музыки
mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
#fire_sound = mixer.Sound('fire.ogg')


#Игровое окно
win_width = 800
win_height = 600
display.set_caption('Space Shooter')
window = display.set_mode((win_width, win_height))


background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))




lost = 0 # счетчик пропущенный кораблей
max_lost = 3 # максимальное количество кораблей для поражения
score = 0 # счетчик сбитых кораблей
win_score = 10 # необходимое количество сбитый короблей для победы
FPS = 60
clock = time.Clock()
game = True
finish = False


#Перезарядка оружия
num_fire = 0
rel_time = False
rel_sec = 1.5


#Пауза в игре
pause = False






player_ship = Player('rocket.png', 5, win_height - 110, 80, 100, 10)


#Создание группы врагов
monsters = sprite.Group()
# Добавить в группу врагов 5 врагов
for i in range(5):
    monster = Enemy('ufo.png', randint(10, win_width - 80), -40, 80, 40, randint(1, 3))
    monsters.add(monster)


#Создание группы астеройдов
asteroids = sprite.Group()
# Добавить в группу астероёдов 3 астеройда
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(10, win_width - 80), -40, 80, 40, randint(1, 2))
    asteroids.add(asteroid)


#Создание группы спрайтов пуль
bullets = sprite.Group()




#Создание надписей
font.init()
stat_font = font.SysFont('Arial', 36)
win_lose_font = font.SysFont('Arial', 96)
win = win_lose_font.render('ПОБЕДА', 1 , (0, 255, 0))
lose = win_lose_font.render('ПОРАЖЕНИЕ', 1, (255, 0, 0))
pause_text = win_lose_font.render('ПАУЗА', 1 , (0, 255, 0))


#Начало игрового цикла

while game:
    #Обработка нажатия на кнопку закрытия окна
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    player_ship.fire()
                    # fire_sound.play()
               
                if num_fire >= 5 and rel_time == False:
                    start_time = timer()
                    rel_time = True
           
            if e.key == K_p:
                if pause == True:
                    finish = False
                    pause = False
                else:
                    finish = True
                    pause = True            
           
   
    if not finish:
        #Отрисовка объектов
        window.blit(background, (0, 0))


        #Текст счетчиков статистики
        monsters_down_text = stat_font.render("Сбито: " + str(score), 1, (255, 255, 255))
        window.blit(monsters_down_text, (10, 30))


        lost_text = stat_font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(lost_text, (10, 60))


        player_ship.reset()
        #отрисовка врагов
        monsters.draw(window)
        #отрисовка астеройдов
        asteroids.draw(window)
        #отрисовка пуль
        bullets.draw(window)


        #перезарядка
        if rel_time == True:
            end_time = timer()


            if end_time - start_time < rel_sec:
                reload_text = stat_font.render('Идет перезагрузка...', 1, (150, 0, 0))
                window.blit(reload_text, (175, 550))
            else:
                num_fire = 0
                rel_time = False


        # Проверка на столкновение пуль и врагов
        collides = sprite.groupcollide(monsters, bullets, True, True)


        for collide in collides:
            score += 1
            monster = Enemy('ufo.png', randint(10, win_width - 80), -40, 80, 40, randint(1, 3))
            monsters.add(monster)
       
        if score >= win_score:
            finish = True
            window.blit(win, (250, 250))
       
        # Обработка поражения в игре
        if sprite.spritecollide(player_ship, monsters, False) or sprite.spritecollide(player_ship, asteroids, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (175, 250))


        player_ship.update()
        display.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        #Обновление позиции для врагов


    # обработка окончания игры (автоматический перезапуск)
    elif pause == True:
        window.blit(pause_text, (250, 250))
        display.update()
    else:
        score = 0
        lost = 0
        num_fire = 0
        rel_time = False


        # обнуление монстров, пуль и астероёдов на экране
        for monster in monsters:
            monster.kill()
       
        for asteroid in asteroids:
            asteroid.kill()
       
        for bullet in bullets:
            bullet.kill()
       
        time.delay(3000)
        for i in range(5):
            monster = Enemy('ufo.png', randint(10, win_width - 80), -40, 80, 40, randint(1, 3))
            monsters.add(monster)
       
        for i in range(3):
            asteroid = Asteroid('asteroid.png', randint(10, win_width - 80), -40, 80, 40, randint(1, 2))
            asteroids.add(asteroid)
       
        finish = False
       


    clock.tick(FPS)



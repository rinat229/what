import pygame
import random
import math

pygame.init()

window_height = 720 
window_width = 1280
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
pygame.display.set_caption("MARIO")
white = (255, 255, 255)
color1 = (136, 0, 27)
color2 = (255, 242, 0)
color3 = (14, 209, 69)
color_heart = (255, 202, 24)
color_tube = (140, 255, 251)
mario1 = pygame.image.load('mario.png') #карт марио, также далее размера марио и т.п.
mario1.set_colorkey(white)
mario = mario1
mario_jump = pygame.image.load('mario_jump.png') #карт марио в прыжке
mario_jump.set_colorkey(white)
bg = pygame.image.load('111.jpg') #background фон
tube = pygame.image.load('tube.png') # препятствие
tube.set_colorkey(color_tube)
cloud1 = pygame.image.load('cloud1.png') # 1 картинка облака, они представлены в виде 3 объектов
cloud1.set_colorkey(color1)
cloud2 = pygame.image.load('cloud2.png') # 2 картинка облака и т.д.
cloud2.set_colorkey(color2)
cloud3 = pygame.image.load('cloud3.png')
cloud3.set_colorkey(color3)
heart = pygame.image.load('heatr1.png') 
heart.set_colorkey(color_heart)
dirt_1 = pygame.image.load('dirt.jpg') # картинка земли, для того чтобы она тоже рисовалась отдельно со своей скоростьб
dirt_2 = pygame.image.load('dirt.jpg')
collision = pygame.image.load('collision.jpg')
dirt_1_x= 0
blink = 0
dirt_2_x= 1640
dirt_width = 1640
cloud_width_1 = 334
cloud_width_2 = 417
cloud_width_3 = 242
mario_x, mario_y = 150, 530
mario_width, mario_height = 63, 86
run = True # переменная для всего игрового цикла, т.е. чтобы можно было выйти из него
isJump = False
dupe_x = 1000
dupe_y = 490
speed = 12
speed_clouds = 5
dupe_height = 150
dupe_width = 76
dupe_x_1 = 1000
dupe_y_1 = 490
jump_count = 10
lives = 3
scores = 0
cloud1_x, cloud1_y = 400, 0
cloud2_x, cloud2_y = 1300, 65
cloud3_x, cloud3_y = 2000, 100
paused = True
# lives_pic = [pygame.image.load('name.jpg'), pygame.image.load('name.jpg'), pygame.image.load('name.jpg')]
above_dupe = False


def draw():
    """Эта функция рисует большинство объектов в окне,
    а именно задний фон, препятствия, самого игрока и жизни"""
    global dupe_height, dupe_x, dupe_y, speed, dupe_x_1, dupe_y_1, paused, blink

    window.blit(bg, (0, 0))#рисуем фон
    window.blit(mario, (mario_x, mario_y))#вставляем картинку марио по его текущим координатам

    if (abs(dupe_x - dupe_x_1) <= 400):#создаем рандомно (координаты) препятствия на разумном расстоянии, чтобы их можно было перепрыгнуть
        dupe_x_1 = random.randint(1280, 2100)

    if dupe_x > -77:# если препятствие ушло за левую часть карты, то отрисовываем его за пределами карты в правой части экрана, также рандомно и разумно
        window.blit(tube, (dupe_x, dupe_y)) # рисуем препятствие по его текущим коордам
        dupe_x -= speed # если труба(препятствие) у нас находится не за пределами, а в окне, то изменяем его х коорду
    else:
        dupe_x = random.randint(window_width, window_width + 820)
        window.blit(tube, (dupe_x, dupe_y))

    if dupe_x_1 > -77:#так как у нас 2 одинаковые трубы, то тут все также, что и выше
        window.blit(tube, (dupe_x_1, dupe_y_1))
        dupe_x_1 -= speed
    else:
        dupe_x_1 = random.randint(window_width, window_width + 520)
        window.blit(tube, (dupe_x_1, dupe_y_1))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: # если зашли в паузу, то вызываем функц паузы
        pause()
    print_text('Scores: ' + str(scores), 1100, 0)#постоянно рисуем текущие очки
    if lives == 3: # если жизни 3, значит рисуем 3 картинки жизни и т.д.
        window.blit(heart, (0, 0))
        window.blit(heart, (67, 0))
        window.blit(heart, (134, 0))
    if lives == 2:
        window.blit(heart, (0, 0))
        window.blit(heart, (67, 0))
    if lives == 1:
        window.blit(heart, (0, 0))
    draw_dirt(); # рисуем землю
    pygame.display.update()


def draw_clouds():
    """фунцкия рисует облака, в этом случае скорость движения облаков уже меньше 
    для большей правдоподобности"""
    global speed_clouds, cloud1_x, cloud1_y, cloud2_x, cloud2_y, cloud3_x, cloud3_y, cloud_width_1, cloud_width_2, cloud_width_3
    if cloud1_x + cloud_width_1 > 0: # если облака в окне(не за пределами карты)
        window.blit(cloud1, (cloud1_x, cloud2_y)) # то рисуем по его текущим коордам
        cloud1_x -= speed_clouds # уменьшаем х координату
    else: 
        cloud1_x = random.randint(window_width, window_width + 220) # если облачко пропало, то рандомно генерируем его за пределами
        cloud1_y = random.randint(68, 100)# то есть в правой части окна

    if cloud2_x + cloud_width_2 > 0:# идея такая же как и для препятствий, у нас есть 3 облака, и мы их рандомно создаем, а потом отрисовываем
        window.blit(cloud2, (cloud2_x, cloud2_y))
        cloud2_x -= speed_clouds
    else:
        cloud2_x = random.randint(window_width + 220, window_width + 420)
        cloud2_y = random.randint(68, 120)

    if cloud3_x + cloud_width_3 > 0:
        window.blit(cloud3, (cloud3_x, cloud3_y))
        cloud3_x -= speed_clouds
    else:
        cloud3_x = random.randint(window_width + 420, window_width + 720)
        cloud3_y = random.randint(80, 120)

    pygame.display.update()


def draw_dirt():
    """Функция для рисования земли: имеется два объекта(два куска, две картинки)
    которые заменяют друг друга в окне"""
    global speed, dirt_1_x, dirt_2_x
    if dirt_1_x >= -dirt_width:
        window.blit(dirt_1, (dirt_1_x, window_height - 105))
        dirt_1_x -= speed
    else:
        dirt_1_x = dirt_width
    if dirt_2_x >=- dirt_width:
        window.blit(dirt_2, (dirt_2_x, window_height - 105))
        dirt_2_x -= speed
    else:
        dirt_2_x = dirt_width

def Jump():
    """Прыжок совершается по параболе"""
    global isJump, jump_count, mario_y, mario
    keys = pygame.key.get_pressed()
    if not (isJump):# проверяет, есть ли прыжок
        if keys[pygame.K_SPACE]: # проверяет нажали ли мы пробел
            isJump = True # присваиваем так, чтобы не было возможности прыгать уже во время прыжка, то есть пока не приземлились
            mario_jump.set_colorkey(white)
            mario = mario_jump
    else:#если мы в прыжке, то
        if jump_count >= -10: # когда jump_count == -10, значит мы уже на земле
            if jump_count > 0: # если мы начали прыгать и летим до вершины параболы, то уменьшаем коорд у
                mario_y -= (jump_count ** 2) / 1.6
            else: # если мы летим от вершины параболы до земли
                mario_y += (jump_count ** 2) / 1.6
            jump_count -= 1
        else:
            isJump = False
            jump_count = 10
            mario = mario1


def print_text(mes, x, y, font_type='font.ttf', font_syze=45, font_color=(0, 0, 0)):
    """Данная функция предназначена для печати текста на экран.
    Принимает текст, координаты, где бы мы хотели написать этот текст,
    шрифт(font_type), размер текста и его цвет"""
    font_type = pygame.font.Font(font_type, font_syze)
    text = font_type.render(mes, True, font_color)
    window.blit(text, (x, y))


def scores_counter():
    """scorec_counter постоянно считает очки(то есть сколько препятствий мы перепрыгнули).
    функция берет координаты препятствий и персонажа, и проверяет, перепрыгнули ли мы их"""
    global scores, above_dupe
    if not above_dupe:#above_dupe проверяет, находимся ли мы в текущий момент над препятствием(изначально False)
        if dupe_x <= mario_x + mario_width / 2 <= dupe_x + dupe_width:
            if mario_y + mario_height <= dupe_y:
                above_dupe = True
    else:
        if jump_count == -10:
            scores += 1
            above_dupe = False

    if not above_dupe:
        if dupe_x_1 <= mario_x + mario_width / 2 <= dupe_x_1 + dupe_width:
            if mario_y + mario_height <= dupe_y_1:
                above_dupe = True
    else:
        if jump_count == -10:
            scores += 1
            above_dupe = False


# def lives_fun():


def BigJump():
    """ Эта интересная штучка выйдет в следующем глобальном обновлении.
    Разработчики ушли в запой"""
    global isJump, jump_count, mario_y

    keys = pygame.key.get_pressed()
    if not (isJump):
        if keys[pygame.K_LSHIFT]:
            isJump = True
    else:
        if jump_count >= -10:
            if jump_count > 0:
                mario_y -= (jump_count ** 2)
            else:
                mario_y += (jump_count ** 2)
            jump_count -= 1
        else:
            isJump = False
            jump_count = 10


def check_collisions():
    """функция предназначена для того, чтобы мы проверяли
    столкнулся ли игрок с препятствием"""
    global mario_y, mario_height, dupe_y, dupe_x, dupe_y_1, dupe_x_1, scores

    if mario_y + mario_height > dupe_y:# обычная проверка, пересекаются ли координаты персонажа и препятствий
        if dupe_x < mario_x < dupe_x + mario_width:
            return False
        elif dupe_x < mario_x + mario_width < dupe_x + mario_width:
            return False

    if mario_y + mario_height > dupe_y_1:
        if dupe_x_1 < mario_x < dupe_x_1 + mario_width:
            return False
        elif dupe_x_1 < mario_x + mario_width < dupe_x_1 + mario_width:
            return False

    return True

def game_over():
    """ Если игрок врезался в трубу более 2 раз, то вызывается game_over().
    Можно либо рестартнуть, либо выйти из игры"""
    paused = True # если вызвали гейм овер
    while paused:
        clock.tick(30)
        print_text('GAME_OVER, PRESS ESC TO EXIT OR ENTER TO REPLAY', 200, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # если нажали крестик, то выходим из игры

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False#если нажали ENTER, то выходим из цикла и начинаем игру заново

        if keys[pygame.K_ESCAPE]:
            pygame.quit() # если нажали ESC, то выходим из игры

        pygame.display.update()

def pause():
    """Функция паузы работает почти также, как и game_over(а точнее наоборот),
    только без кнопки реплея, и без обнуления lives and scores"""
    global run
    paused = True
    while paused:
        clock.tick(30)
        print_text('PAUSE. PRESS ENTER TO CONTINUE', 300, 400)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        pygame.display.update()


def running():
    """Основная функция игры, в ней содержится тело цикла"""
    global run, lives, dupe_x, dupe_x_1, scores
    while run:
        clock.tick(30) # 30 фпс

        if not (check_collisions()):#если столкнулись с препятствием, то
            dupe_x = random.randint(1280, 1800) # заново генерируем препятствия за пределами окна(в правой части)
            dupe_x_1 = random.randint(1280, 1800)
            lives -= 1 # каждый раз сталкиваясь, уменьшаем жизьку
            if lives == 0: # если все жизьки потрачены, то
                game_over() # вызываем game_over
                lives = 3 # заново 3 жизьки
                scores = 0 # обнуляем очки
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        draw()#рисуем всевозможную чепуху
        draw_clouds()# и облака
        if keys[pygame.K_ESCAPE]:
            pause()
        # BigJump()
        scores_counter()#подсчитываем очки
        Jump()#постоянно проверяем , прыгаем ли мы
       

if __name__ == "__main__":
    running()
    pygame.quit()
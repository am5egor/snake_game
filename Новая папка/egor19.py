from pygame import *
from random import randint
from time import sleep

screen = display.set_mode((700, 500))
display.set_caption('змейка')
screen.fill((59, 100, 47))
clock = time.Clock()

play = True
head = Rect(350,250, 20,20)
speed = 20
direction = [0,-speed]
color = (100, 0, 0)
score = 0
timer = 20
step = 30
seconds = 5
level_1 = True
level_2 = True

font.init()
font = font.Font(None, 24)
score_text = font.render('счёт: ' + str(score), True, (20, 20, 50))
timer_text = font.render('время: ' + str(timer), True, (20, 20, 50))
lose_pic = transform.scale(image.load('istockphoto-1148824291-612x612.jpg'), [700, 500])
win_pic = transform.scale(image.load('победа.jpg'), [700, 500])

def load_image(pic, x, y):
    images = transform.scale(image.load(pic), [20,20])
    rect = images.get_rect(center = (x, y))
    #images.set_colorkey(images.get_at((0,0)))
    return images, rect

def random_color():
    r = randint(0,255)
    g = randint(0,205)
    b = randint(0,155)
    return(r, g, b)

def move(head, snake):
    global direction
    KEY = key.get_pressed()

    if KEY[K_w] and direction[1] == 0:
        direction = [0,-speed]
    elif KEY[K_s] and direction[1] == 0:
        direction = [0, speed]
    elif KEY[K_a] and direction[0] == 0:
        direction = [-speed, 0]
    elif KEY[K_d] and direction[0] == 0:
        direction = [speed, 0]

    if head.bottom > 500:
        head.bottom = 25
    elif head.top < 0:
        head.top = 475
    elif head.left < 0:
        head.left = 675
    elif head.right > 700:
        head.right = 25
    for index in range(len(snake)-1, 0, -1):
        snake[index].x = snake[index-1].x
        snake[index].y = snake[index-1].y

    head.move_ip(direction)

def catch_apple(seconds):
    global score, head_rect, apple_rect, timer, snake
    if head_rect.colliderect(apple_rect):
        score += 1
        apple_rect.x = randint(0,670)
        apple_rect.y = randint(0,470)
        timer += seconds
        snake[-1].x += step - speed
        snake.append(snake[-1].copy())

def catch_mushroom():
    global score, head_rect, mushroom_rect, snake
    if head_rect.colliderect(mushroom_rect):
        if len(snake) > 1:
            score -= 1
            mushroom_rect.x = randint(0,670)
            mushroom_rect.y = randint(0,470)
            snake.remove(snake[-1])  
        else:
            lose()

def close(picture):
    global play
    play = False
    screen.blit(picture, (0,0))
    display.update()
    sleep(5)

def level():
    global score, seconds
    if score >= 2:
        seconds = 4
    elif score >= 1:
        seconds = 4
    else:
        seconds = 5
    return seconds

def mashrooms():
    global score, level_1, level_2
    if score >= 2 and level_2:
        level_2 = False
        mushroom_2, mushroom_rect_2 = load_image('Mario-Mushroom-PNG-Pic-Background.png', randint(0,670), randint(0,470))
        return mushroom_2, mushroom_rect_2
    elif score >= 1 and level_1:
        level_1 = False
        mushroom_1, mushroom_rect_1 = load_image('Mario-Mushroom-PNG-Pic-Background.png', randint(0,670), randint(0,470))
        return mushroom_1, mushroom_rect_1


def crash_snake():
    global snake, head_rect, body_rect
    for sigment in snake[1:]:
        if head_rect.colliderect(sigment):
            return True
    return False

head_snake, head_rect = load_image('head.png', 350, 250)
body_snake, body_rect = load_image('body.png', 350, 250 + step)
apple, apple_rect = load_image('apple-MaLv9SR1j-transformed.png', randint(0,670), randint(0,470))
mushroom, mushroom_rect = load_image('Mario-Mushroom-PNG-Pic-Background.png', randint(0,670), randint(0,470))

snake = [head_rect, body_rect]

wait = 20

while play:
    for e in event.get():
        if e.type == QUIT:
            play = False

    screen.fill((59, 100, 47))

    if wait > 0:
        wait -= 1
    else:
        timer -= 1
        wait = 20

    timer_text = font.render('время: ' + str(timer), True, (20, 20, 50))
    screen.blit(timer_text, (10, 10))
    score_text = font.render('счёт: ' + str(score), True, (20, 20, 50))
    screen.blit(score_text, (10, 30))

    screen.blit(head_snake, head_rect)
    screen.blit(apple, apple_rect)
    screen.blit(mushroom, mushroom_rect)
    '''if score >= 1:
        mushroom_1, mushroom_rect_1 = mashrooms()
        screen.blit(mushroom_1, mushroom_rect_1)
    if score >= 2:
        mushroom_2, mushroom_rect_2 = mashrooms()
        screen.blit(mushroom_2, mushroom_rect_2)'''

    for segment in snake[1:]:
        screen.blit(body_snake, segment)

    move(head_rect, snake)
    catch_apple(seconds)
    catch_mushroom()
    seconds = level()

    if timer == 0 or crash_snake():
        close(lose_pic)
    
    if score >= 30:
        close(win_pic)

    display.update()
    clock.tick(20)

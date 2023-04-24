import sys
import pygame, time
from random import randint

class GridPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

AREA = GridPoint(640,480)
SPEED_DELAY = 0.1
STEP_SIZE = 20
BG_COLOR = (51,154,51)

pygame.init()
game_screen = pygame.display.set_mode((AREA.x, AREA.y))
continue_game = True

snake_head = pygame.sprite.Sprite()
snake_head.tail = []
snake_head.image = pygame.image.load("snake.png")
snake_head.rect = snake_head.image.get_rect()
snake_group = pygame.sprite.GroupSingle(snake_head)

strawberry = pygame.sprite.Sprite()
strawberry.live = False
strawberry.image = pygame.image.load("strawberry.png")
strawberry.rect = strawberry.image.get_rect()
apple_group = pygame.sprite.GroupSingle(strawberry)
STEP_SIZE = snake_head.rect.width


def moveSprite(sprite):
    # Двигаем спрайт змейки
    if sprite.direction == "U":
        sprite.rect.top -= STEP_SIZE
    elif sprite.direction == "D":
        sprite.rect.top += STEP_SIZE
    elif sprite.direction == "L":
        sprite.rect.left -= STEP_SIZE
    elif sprite.direction == "R":
        sprite.rect.left += STEP_SIZE

    if sprite.rect.left < 0:
        sprite.rect.left = 0
    if sprite.rect.top < 0:
        sprite.rect.top = 0
    if sprite.rect.bottom > AREA.y:
        sprite.rect.bottom = AREA.y
    if sprite.rect.right > AREA.x:
        sprite.rect.right = AREA.x

def handleEvents():
    # Обрабатывает любые события и возвращает False, если игра должна завершиться, True в противном случае
    for event in pygame.event.get():
        if isExitGameEvent(event):
            return False
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w)  and snake_head.direction != 'D':
                snake_head.direction = "U"
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake_head.direction != 'U':
                snake_head.direction = "D"
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake_head.direction != 'R':
                snake_head.direction = "L"
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake_head.direction != 'L':
                snake_head.direction = "R"
    return True

def isExitGameEvent(event):
    # Проверяем кончилась ли игра
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        sys.exit()
    return False
def waitForKeyPress():
    # Ждём любое нажатие клавиши
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return

def createBerries():
    # Если яблок нет, создаём одно в случайном месте.
    if not strawberry.live:
        strawberry.rect.top = randint(0, AREA.y - STEP_SIZE)
        strawberry.rect.top -= strawberry.rect.top % STEP_SIZE
        strawberry.rect.left = randint(0, AREA.x - STEP_SIZE)
        strawberry.rect.left -= strawberry.rect.left % STEP_SIZE
        strawberry.live = True

def eatAvailiableBerries(eater):
    # Проверяем, может ли змейка съесть яблоко, если да, то съедаем его.
    if (eater.rect.left == strawberry.rect.left) & (eater.rect.top == strawberry.rect.top):
        return True
    else:
        return False

def snakeIsTangled(snake):
    # Проверяем, если змейка запуталась
    y = snake.rect.top
    x = snake.rect.left
    for tailSeg in snake.tail:
        if y == tailSeg.y and x == tailSeg.x:
            return True
    return False

def updateSnake():
    # Обновляем положение змейки и хвоста, возвращаем False, если змейка запуталась
    snake_head.tail.append(GridPoint(snake_head.rect.left, snake_head.rect.top))
    moveSprite(snake_head)
    if eatAvailiableBerries(snake_head):
        strawberry.live = False
    elif snakeIsTangled(snake_head):
        return False
    else:
        snake_head.tail.pop(0)

    return True

def drawSnake():
    # Отрисовываем змейку
    halfStep = STEP_SIZE/2
    snake_group.draw(game_screen)
    for tailSeg in snake_head.tail:
        pygame.draw.circle(game_screen, (10,200,10), (tailSeg.x+halfStep,tailSeg.y+halfStep), STEP_SIZE/3, 2)

def printText(game_screen, text, yLoc, size, color = (255,255,255)):
    # Показываем текст на экране
    gameFont = pygame.font.Font(None, size)
    label = gameFont.render(text, True, color)
    lblHeight = label.get_rect().bottom - label.get_rect().top
    lblWidth = label.get_rect().right - label.get_rect().left
    game_screen.blit(label, (AREA.x/2 - lblWidth/2, yLoc))

def printEndOfGameSummary(game_screen, score):
    # Показываем конечный счёт и ждём кнопку для закрытия
    game_screen.fill(BG_COLOR)
    time.sleep(1)
    printText(game_screen, "Game Over", 150, 35)
    printText(game_screen, "Score: {}".format(score), 200, 30)
    pygame.display.update()
    waitForKeyPress()

snake_head.direction = "D"
game_speed_mofifier = SPEED_DELAY
while continue_game:
    # тело цикла игры
    time.sleep(game_speed_mofifier)
    continue_game = handleEvents()
    continue_game = updateSnake()

    game_screen.fill(BG_COLOR)
    printText(game_screen, "{}".format(len(snake_head.tail)), 10, 30, (255, 255, 255))
    drawSnake()

    createBerries()
    apple_group.draw(game_screen)

    pygame.display.update()

printEndOfGameSummary(game_screen, len(snake_head.tail)-1)
pygame.quit()

import pygame
import math
import random
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from operator import itemgetter

class cube():
    rows = 20
    width = 500

    def __init__(self, start, dirX = 1, dirY = 0, color = (50, 255, 0)):
        self.pos = start
        self.dirX = dirX
        self.dirY = dirY
        self.color = color


    def move(self, dirX, dirY):
        self.dirX = dirX
        self.dirY = dirY
        self.pos = (self.pos[0] + self.dirX, self.pos[1] + self.dirY)

    def draw(self, surface, eyes = False):
        gap = self.width // self.rows #gab between cubes
        row = self.pos[0]
        col = self.pos[1]

        pygame.draw.rect(surface, self.color, (row * gap + 1, col * gap + 1, gap - 2, gap - 2)) #ensures gaps are shown when snake goes over grid

        if eyes:
            centre = gap // 2 #center of cell
            radius = 3
            eyeLeft = (row * gap + centre - radius, col * gap + 8)
            eyeRight = (row * gap + gap - radius * 2, col * gap + 8)
            pygame.draw.circle(surface, (251, 255, 0), eyeLeft, radius)
            pygame.draw.circle(surface, (251, 255, 0), eyeRight, radius)

            radius = 1
            pupilLeft = (row * gap + centre - (radius + 2) , col * gap + 8)
            pupilRight = (row * gap + gap - ((radius * 2) + 4), col * gap + 8)
            pygame.draw.circle(surface, (0, 0, 0), pupilLeft, radius)
            pygame.draw.circle(surface, (0, 0, 0), pupilRight, radius)


class snake():
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirX = 0
        self.dirY = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirX = -1
                    self.dirY = 0
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

                elif keys[pygame.K_RIGHT]:
                    self.dirX = 1
                    self.dirY = 0
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

                elif keys[pygame.K_UP]:
                    self.dirX = 0
                    self.dirY = -1
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

                elif keys[pygame.K_DOWN]:
                    self.dirX = 0
                    self.dirY = 1
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        for i, cube in enumerate(self.body):
            dir = cube.pos[:] #grab direction value of cube object (body is cube object)
            if dir in self.turns:
                turn = self.turns[dir] #turns at the cube when turn input was entered
                cube.move(turn[0], turn[1])

                if i == len(self.body) - 1: #removes turn keystroke from turns list, otherwise snake would turn each time it goes over that location
                    self.turns.pop(dir)

            else:
                if cube.dirX == -1 and cube.pos[0] <= 0:
                    cube.pos = (cube.rows - 1, cube.pos[1])
                elif cube.dirX == 1 and cube.pos[0] >= cube.rows - 1:
                    cube.pos = (0, cube.pos[1])
                elif cube.dirY == 1 and cube.pos[1] >= cube.rows - 1:
                    cube.pos = (cube.pos[0], 0)
                elif cube.dirY == -1 and cube.pos[1] <= 0:
                    cube.pos = (cube.pos[0], cube.rows - 1)
                else:
                    cube.move(cube.dirX, cube.dirY)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.dirX = 0
        self.dirY = 1
        self.turns = {}

    def addCube(self):
        tail = self.body[-1]
        dx = tail.dirX
        dy = tail.dirY

        #adds cube to snake based on its movement direction
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirX = dx
        self.body[-1].dirY = dy

    def draw(self, surface):
        for i, cube in enumerate(self.body):
            if i == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)

def drawGrid(width, rows, surface):
    gap = width // rows #gap between boxes
    x = 0
    y = 0

    for line in range(rows):
        x = x + gap
        y = y + gap

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))


def redrawWindow(surface):
    global rows, width, snake, snack
    surface.fill((66, 135, 245))
    snake.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    font = pygame.font.SysFont('comicsans', 40)
    text = font.render('Score: ' + str(len(snake.body)), 1, (25, 0, 255))
    surface.blit(text, (0, 0))
    pygame.display.update()


def randomSnack(rows, snake):
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        if len(list(filter(lambda snack: snack.pos == (x, y), positions))) > 0: #ensure snack isn's placed on top of snake
            continue
        else:
            break
    return (x, y)


def message_box(title, score):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    reply = messagebox.askyesno(title, score)

    if reply == False:
        playAgain = messagebox.askyesno("Play again?", "Would you like to play again?")
        if playAgain == False:
            flag = False
            pygame.display.quit()
            pygame.quit()

    elif reply == True:
        name = simpledialog.askstring("Save Score", "What is your name?")

        # highscores = get_highscore()
        # highscores.append(name: score)
        #
        # store_highscore(sorted(highscores, key=itemgetter(1), reverse=True))

        playAgain = messagebox.askyesno("Play again?", "Would you like to play again?")
        if playAgain == False:
            flag = False
            pygame.display.quit()
            pygame.quit()


    try:
        root.destory()
    except:
        pass

def store_highscore(highscores):
    with open('Scores.json', 'w') as scores:
        json.dump(highscores, scores)

def get_highscore():
    try:
        with open('Scores.json', 'r') as scores:
            highscores = json.load(scores)  # Read the json file.
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist.
    # Sorted by the score.
    return sorted(highscores, key = itemgetter(1), reverse = True)

def main_menu(surface):
    pygame.font.init()
    title_font = pygame.font.SysFont("comicsans", 70)
    title = title_font.render("Welcome to Snake", True, (66, 135, 245))
    play_game_font = pygame.font.SysFont('comicsans',35)
    play_game_button = play_game_font.render('Play Game' , True , (0,0,0))
    quit_game_font = pygame.font.SysFont('comicsans',35)
    quit_game_button = quit_game_font.render('Quit Game' , True , (0,0,0))
    scoreboard_font = pygame.font.SysFont('comicsans',35)
    scoreboard_button = scoreboard_font.render('Scoreboard' , True , (0,0,0))

    run = True

    while run:
        surface.blit(title, (surface.get_width() / 2 - title.get_width() / 2, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 <= mouse[0] <= surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 + 160 and surface.get_height() / 2 - 10 <= mouse[1] <= surface.get_height() / 2 - 10 + 40:
                    play_game()
                elif surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 <= mouse[0] <= surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 + 160 and surface.get_height() / 2 + 50 <= mouse[1] <= surface.get_height() / 2 + 50 + 40:
                    pass
                elif surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 <= mouse[0] <= surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 + 160 and surface.get_height() / 2 + 110 <= mouse[1] <= surface.get_height() / 2 + 110 + 40:
                    run = False
                    pygame.quit()

        # Stores the (x,y) coordinates as a tuple
        mouse = pygame.mouse.get_pos()

        # change color of button upon hover
        if surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 <= mouse[0] <= surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 + 160 and surface.get_height() / 2 - 10 <= mouse[1] <= surface.get_height() / 2 - 10 + 40:
            pygame.draw.rect(surface, (10, 150, 0), [surface.get_width() / 2 - play_game_button.get_width() / 2 - 15, surface.get_height() / 2 - 10, 160, 40])
        elif surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 <= mouse[0] <= surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 + 160 and surface.get_height() / 2 + 50 <= mouse[1] <= surface.get_height() / 2 + 50 + 40:
            pygame.draw.rect(surface, (10, 150, 0), [surface.get_width() / 2 - play_game_button.get_width() / 2 - 15, surface.get_height() / 2 + 50, 160, 40])
        elif surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 <= mouse[0] <= surface.get_width() / 2 - play_game_button.get_width() / 2 - 15 + 160 and surface.get_height() / 2 + 110 <= mouse[1] <= surface.get_height() / 2 + 110 + 40:
            pygame.draw.rect(surface, (10, 150, 0), [surface.get_width() / 2 - play_game_button.get_width() / 2 - 15, surface.get_height() / 2 + 110, 160, 40])
        else:
            pygame.draw.rect(surface, (16, 240, 0), [surface.get_width() / 2 - play_game_button.get_width() / 2 - 15, surface.get_height() / 2 - 10, 160, 40])
            pygame.draw.rect(surface, (16, 240, 0), [surface.get_width() / 2 - play_game_button.get_width() / 2 - 15, surface.get_height() / 2 + 50, 160, 40])
            pygame.draw.rect(surface, (16, 240, 0), [surface.get_width() / 2 - play_game_button.get_width() / 2 - 15, surface.get_height() / 2 + 110, 160, 40])

        # superimpose the button text onto the button
        surface.blit(play_game_button, (surface.get_width() / 2 - play_game_button.get_width() / 2, surface.get_height() / 2))
        surface.blit(scoreboard_button, (surface.get_width() / 2 - scoreboard_button.get_width() / 2, surface.get_height() / 2 + 60))
        surface.blit(quit_game_button, (surface.get_width() / 2 - quit_game_button.get_width() / 2, surface.get_height() / 2 + 120))
    pygame.quit()


def play_game():
    global width, rows, snake, snack, flag
    width = 500
    rows = 20
    run = True
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Snake")
    snake = snake((255, 0, 0), (9, 8))
    snack = cube(randomSnack(rows, snake), color = (255, 0, 0))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('comicsans', 30, True)

    while run:
        pygame.time.delay(50)
        clock.tick(10) #limits snake movement to 10 block/second
        snake.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

        if snake.body[0].pos == snack.pos:
            snake.addCube()
            snack = cube(randomSnack(rows, snake), color = (255, 0, 0))

        # check if body position is in list of all possible positions of the snake
        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda square: square.pos, snake.body[x + 1:])):
                #print ("Score: ", len(snake.body))
                message_box("Game Over", "Score: {}! Would you like to save score?".format(len(snake.body)))
                snake.reset((9, 8))
                break

        redrawWindow(win)
    pygame.quit()

def main():
    global width
    width = 500
    rows = 20
    run = True
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Snake")
    main_menu(win)



main()

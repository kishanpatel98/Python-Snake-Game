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

def main():
    global width, rows, snake, snack, flag
    width = 500
    rows = 20
    flag = True
    win = pygame.display.set_mode((width, width))
    snake = snake((255, 0, 0), (9, 8))
    snack = cube(randomSnack(rows, snake), color = (255, 0, 0))
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10) #limits snake movement to 10 block/second
        snake.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
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


    pass

main()

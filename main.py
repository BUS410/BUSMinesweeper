from pprint import pprint
from random import randrange
from time import time
from tkinter import Tk, messagebox

import pygame


WINDOW_SIZE = 640
FPS = 30


class Game:

    def __init__(self, size, mines):
        self.status = 'play'
        self.size = size
        self.field = [[None for _ in range(size)] for _ in range(size)]
        self.cell_size = WINDOW_SIZE//len(self.field)
        for _ in range(mines):
            while True:
                x, y = randrange(0, size), randrange(0, size)
                if self.field[y][x] == None:
                    self.field[y][x] = -1
                    break
        pygame.init()
        pygame.display.set_icon(pygame.image.load('icon.png'))
        self.window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('BUSMinesweeper')
        pygame.font.init()
        self.font = pygame.font.SysFont('consolas', WINDOW_SIZE//size)
        Tk().withdraw()

    def _mines_around(self, x, y):
        res = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (0 <= x+j < self.size) and (0 <= y+i < self.size):
                    res += 1 if self.field[y+i][x+j] != None and self.field[y+i][x+j] < 0 else 0
        return res

    def _new_around(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not ((0 <= x+j < self.size) and (0 <= y+i < self.size)):
                    continue
                if self.field[y+i][x+j] == None:
                    yield (x+j, y+i)

    def step(self, x, y):
        if self.field[y][x] == -1:
            self.field[y][x] = 9
            self.status = 'lose'
            return
        old = [(x, y)]
        new = []
        while True:
            for x, y in old:
                self.field[y][x] = self._mines_around(x, y)
                if self.field[y][x]:
                    continue
                [new.append(point) for point in self._new_around(x, y) if point not in new]
            if not new:
                break
            old, new = new, []
        is_win = True
        for row in self.field:
            if None in row:
                is_win = False
                break
        if all(None not in row for row in self.field):
            self.status = 'win'

    def draw(self):
        self.window.fill((128, 128, 255))
        for y, row in enumerate(self.field):
            for x, cell in enumerate(row):
                if cell in (None, -1):
                    pygame.draw.rect(self.window, (225, 225, 128),
                        (x*self.cell_size, y*self.cell_size,
                        self.cell_size, self.cell_size), 1
                    )
                elif cell < -1:
                    pygame.draw.rect(self.window, (255, 128, 128),
                        (x*self.cell_size, y*self.cell_size,
                        self.cell_size, self.cell_size)
                    )
                    pygame.draw.rect(self.window, (192, 192, 128),
                        (x*self.cell_size, y*self.cell_size,
                        self.cell_size, self.cell_size), 1
                    )
                elif cell == 9:
                    pygame.draw.rect(self.window, (255, 0, 0),
                        (x*self.cell_size, y*self.cell_size,
                        self.cell_size, self.cell_size)
                    )
                    pygame.draw.rect(self.window, (192, 192, 128),
                        (x*self.cell_size, y*self.cell_size,
                        self.cell_size, self.cell_size), 1
                    )
                else:
                    pygame.draw.rect(self.window, (255, 255, 128),
                        (x*self.cell_size, y*self.cell_size,
                        self.cell_size, self.cell_size)
                    )
                    pygame.draw.rect(self.window, (192, 192, 128),
                        (x*self.cell_size, y*self.cell_size,
                        self.cell_size, self.cell_size), 1
                    )
                    if cell:
                        text = self.font.render(str(cell), 1, (min(255, 60 * cell), 255 - min(255, 60 * cell), 0))
                        self.window.blit(text,
                            (
                                x*self.cell_size + max((self.cell_size - text.get_width()) // 2, 0),
                                y*self.cell_size + max((self.cell_size - text.get_height()) // 2, 0)
                            )
                        )
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        start = time()
        while True:
            if self.status == 'win':
                messagebox.showinfo('Победа! :)', f'Повезло, повезло...\nВремя: {round(time()-start, 2)} секудны.')
                return
            elif self.status == 'lose':
                messagebox.showerror('Поражение! :(', f'Не повезло, не повезло...\nВремя {round(time()-start, 2)} секудны.')
                return
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    x //= WINDOW_SIZE // len(self.field)
                    y //= WINDOW_SIZE // len(self.field)
                    if event.button == 1 and (self.field[y][x] == None or self.field[y][x] >= -1):
                        self.step(x, y)
                    elif event.button == 3:
                        if self.field[y][x] == -1:
                            self.field[y][x] = -2
                        elif self.field[y][x] == None:
                            self.field[y][x] = -3
                        elif self.field[y][x] == -2:
                            self.field[y][x] = -1
                        elif self.field[y][x] == -3:
                            self.field[y][x] = None
            self.draw()
            clock.tick(FPS)


if __name__ == '__main__':
    Game(9, 10).run()

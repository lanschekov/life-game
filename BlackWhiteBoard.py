from math import floor

import pygame
from pygame import Surface, SurfaceType

BLACK = 0
WHITE = 1
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [[BLACK] * width for _ in range(height)]
        # значения по умолчанию
        self.x = 10
        self.y = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, x: int, y: int, cell_size: int) -> None:
        self.x = x
        self.y = y
        self.cell_size = cell_size

    def render(self, screen: Surface | SurfaceType) -> None:
        screen.fill((0, 0, 0))
        cur_x, cur_y = self.x, self.y
        for row in self.board:
            for cell in row:
                # Cell borders
                pygame.draw.rect(screen, WHITE_COLOR,
                                 (cur_x, cur_y, self.cell_size, self.cell_size), width=1)
                # Cell pouring
                pygame.draw.rect(screen, BLACK_COLOR if cell is BLACK else WHITE_COLOR,
                                 (cur_x + 1, cur_y + 1, self.cell_size - 2, self.cell_size - 2), width=0)

                cur_x += self.cell_size
            cur_x = self.x
            cur_y += self.cell_size

    def get_click(self, x: int, y: int) -> None:
        cell = self.get_cell(y, x)
        if not cell:
            return
        self.on_click(*cell)

    def get_cell(self, y: int, x: int) -> tuple[int, int] | None:
        if not self.check_click(y, x):
            return None
        rel_y = y - self.y
        rel_x = x - self.x
        cell_row = floor(rel_y / self.cell_size)
        cell_col = floor(rel_x / self.cell_size)
        return cell_row, cell_col

    def check_click(self, y: int, x: int) -> bool:
        return self.x <= x <= self.x + self.width * self.cell_size \
               and self.y <= y <= self.y + self.height * self.cell_size

    def on_click(self, cell_row: int, cell_col: int) -> None:
        if self.board[cell_row][cell_col] is BLACK:
            self.board[cell_row][cell_col] = WHITE
        else:
            self.board[cell_row][cell_col] = BLACK


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    board = Board(7, 5)
    board.render(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(*event.pos)

        board.render(screen)
        pygame.display.flip()

    pygame.quit()

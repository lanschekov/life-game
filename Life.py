import copy

import pygame
from pygame import Surface, SurfaceType

from BlackWhiteBoard import Board, WHITE_COLOR, BLACK_COLOR

LIVE_CELL = 1
DEAD_CELL = 0
LIVE_COLOR = (0, 255, 0)
DEAD_COLOR = BLACK_COLOR


class Life(Board):
    def __init__(self, width: int, height: int):
        super(Life, self).__init__(width, height)
        self.board = [[DEAD_CELL] * width for _ in range(height)]
        self.is_populating = False
        self.board_stack = []

    def render(self, screen: Surface | SurfaceType) -> None:
        screen.fill((0, 0, 0))
        cur_x, cur_y = self.x, self.y
        for row in self.board:
            for cell in row:
                # Cell borders
                pygame.draw.rect(screen, WHITE_COLOR,
                                 (cur_x, cur_y, self.cell_size, self.cell_size), width=1)
                # Cell pouring
                pygame.draw.rect(screen, DEAD_COLOR if cell is DEAD_CELL else LIVE_COLOR,
                                 (cur_x + 1, cur_y + 1, self.cell_size - 2, self.cell_size - 2), width=0)

                cur_x += self.cell_size
            cur_x = self.x
            cur_y += self.cell_size

    def on_click(self, cell_row: int, cell_col: int) -> None:
        if self.board[cell_row][cell_col] is DEAD_CELL:
            self.board[cell_row][cell_col] = LIVE_CELL
        else:
            self.board[cell_row][cell_col] = DEAD_CELL

    def next_move(self):
        temp = copy.deepcopy(self.board)
        screen.fill((0, 0, 0))
        for row in range(self.height):
            for col in range(self.width):
                neighbors = self.get_neighbors(row, col)
                live_amount = len([cell for cell in neighbors if cell is LIVE_CELL])
                if self.board[row][col] is DEAD_CELL and live_amount == 3:
                    temp[row][col] = LIVE_CELL
                elif self.board[row][col] is LIVE_CELL and live_amount not in (2, 3):
                    temp[row][col] = DEAD_CELL

        self.board_stack.append(self.board)
        self.board = temp
        if self.game_over():
            self.is_populating = False
            self.board_stack.clear()

    def get_neighbors(self, cell_row: int, cell_coll: int) -> tuple:
        res = []
        neighbors_ind = ((cell_row - 1, cell_coll - 1), (cell_row - 1, cell_coll),
                         (cell_row - 1, cell_coll + 1), (cell_row, cell_coll - 1),
                         (cell_row, cell_coll + 1), (cell_row + 1, cell_coll - 1),
                         (cell_row + 1, cell_coll), (cell_row + 1, cell_coll + 1))
        for row, col in neighbors_ind:
            if 0 <= row <= self.height - 1 and 0 <= col <= self.width - 1:
                res.append(self.board[row][col])
        return tuple(res)

    def game_over(self) -> bool:
        if all(cell is DEAD_CELL for row in self.board for cell in row):
            return True
        if self.board in self.board_stack:
            return True
        return False


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    fps = 10
    clock = pygame.time.Clock()
    board = Life(30, 30)
    board.set_view(0, 0, cell_size=15)
    # board.render(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT \
                    and not board.is_populating:
                board.get_click(*event.pos)
            if event.type == pygame.MOUSEWHEEL:
                # Scrolling down
                if event.y < 0:
                    fps += 3
                else:
                    fps -= 3
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT) \
                    and not board.is_populating:
                board.is_populating = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and board.is_populating:
                board.is_populating = False

        if board.is_populating:
            board.next_move()
        board.render(screen)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

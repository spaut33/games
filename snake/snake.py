import random
import pygame

from dataclasses import dataclass
from pygame.surface import Surface

# FPS of the game window


FPS = 10
TITLE = 'Snake game by spaut'
MAX_CHAINS = 32
SNAKE_COLOR = (55, 120, 255)
FOOD_COLOR = (120, 255, 55)
TEXT_COLOR = (200, 200, 200)
BG_COLOR = (0, 0, 0)
WIDTH = 800
HEIGHT = 600
SNAKE_BLOCK_SIZE = 20


@dataclass
class DisplayWindow:
    display: Surface


@dataclass
class Snake(DisplayWindow):
    snake_length: int = 1
    max_chains: int = MAX_CHAINS
    color: tuple = SNAKE_COLOR
    snake_block_size: int = SNAKE_BLOCK_SIZE
    dx: int = 0
    dy: int = 0
    x: float = WIDTH // 2
    y: float = HEIGHT // 2
    background_color: tuple = BG_COLOR
    snake_head: tuple = (x, y)

    def __post_init__(self) -> None:
        self.snake_chain: list = [self.snake_head]

    def change_direction(self, dx: int = 0, dy: int = 0) -> None:
        self.dx = dx
        self.dy = dy

    def draw(self) -> None:
        self.x += self.dx
        self.y += self.dy
        self.chain()
        self.display.fill(self.background_color)
        for x, y in self.snake_chain:
            pygame.draw.rect(
                self.display,
                self.color,
                [x, y, self.snake_block_size, self.snake_block_size],
            )

    def get_position(self) -> tuple:
        return self.x, self.y

    def grow(self) -> None:
        self.snake_length += 1

    def chain(self) -> None:
        self.snake_head = (self.x, self.y)
        self.snake_chain.append(self.snake_head)
        if len(self.snake_chain) > self.snake_length:
            del self.snake_chain[0]

    def self_eat(self) -> bool:
        for block in self.snake_chain[:-1]:
            if block == self.snake_head:
                return True
        return False


@dataclass
class Food(DisplayWindow):
    food_size: int = SNAKE_BLOCK_SIZE
    color: tuple = FOOD_COLOR

    def __post_init__(self) -> None:
        self.x = (
            round(
                random.randrange(0, WIDTH - self.food_size) // self.food_size
            )
            * self.food_size
        )
        self.y = (
            round(
                random.randrange(0, HEIGHT - self.food_size) // self.food_size
            )
            * self.food_size
        )

    def draw(self) -> None:
        pygame.draw.rect(
            self.display,
            self.color,
            [self.x, self.y, self.food_size, self.food_size],
        )

    def get_position(self) -> tuple:
        return self.x, self.y


@dataclass
class GameManager(DisplayWindow):
    points: int = 0

    def increase_points(self) -> None:
        self.points += 1

    def show_score(self) -> None:
        score_font = pygame.font.SysFont("tahoma", 14)
        value = score_font.render(
            "Score: " + str(self.points), True, TEXT_COLOR
        )
        self.display.blit(value, [4, 2])


@dataclass
class GameWindow:
    pygame.init()
    game_over: bool = False
    _width: int = WIDTH
    _height: int = HEIGHT
    _title: str = TITLE
    display: Surface = pygame.display.set_mode((_width, _height))
    pygame.display.set_caption(_title)
    game: GameManager = GameManager(display)
    food: Food = Food(display)
    snake: Snake = Snake(display)

    def main_loop(self) -> None:
        clock = pygame.time.Clock()
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # x change = -10; y change = 0
                        self.snake.change_direction(dx=-SNAKE_BLOCK_SIZE)
                    elif event.key == pygame.K_RIGHT:
                        # x change = 10; y change = 0
                        self.snake.change_direction(dx=SNAKE_BLOCK_SIZE)
                    elif event.key == pygame.K_UP:
                        # y change = -10; x change = 0
                        self.snake.change_direction(dy=-SNAKE_BLOCK_SIZE)
                    elif event.key == pygame.K_DOWN:
                        # y change = 10; x change = 0
                        self.snake.change_direction(dy=SNAKE_BLOCK_SIZE)
            if self.check_bounds() or self.snake.self_eat():
                self.game_over = True
            if self.check_food():
                self.snake.grow()
                self.game.increase_points()
                self.food = Food(self.display)

            self.snake.draw()
            self.food.draw()
            self.game.show_score()
            pygame.display.update()
            clock.tick(FPS)

    def check_bounds(self) -> bool:
        x, y = self.snake.get_position()
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            return True
        return False

    def check_food(self) -> bool:
        x_snake, y_snake = self.snake.get_position()
        x_food, y_food = self.food.get_position()
        if x_snake == x_food and y_snake == y_food:
            return True
        return False


def main() -> None:
    window = GameWindow()
    window.main_loop()
    print('Game over. Exiting...')


if __name__ == "__main__":
    main()

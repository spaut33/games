from food import Food

import pygame

from dataclasses import dataclass
from pygame.surface import Surface

from settings import Settings


@dataclass
class Snake:
    display: Surface
    snake_length: int = 1
    max_chains: int = Settings.MAX_CHAINS
    color: tuple = Settings.SNAKE_COLOR
    snake_block_size: int = Settings.SNAKE_BLOCK_SIZE
    dx: int = 0
    dy: int = 0
    x: float = Settings.WIDTH // 2
    y: float = Settings.HEIGHT // 2
    background_color: tuple = Settings.BG_COLOR
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
class GameManager:
    display: Surface
    points: int = 0

    def increase_points(self) -> None:
        self.points += 1

    def show_score(self) -> None:
        score_font = pygame.font.SysFont(
            Settings.FONT_FAMILY, Settings.FONT_SIZE
        )
        value = score_font.render(
            "Score: " + str(self.points), True, Settings.TEXT_COLOR
        )
        self.display.blit(value, [4, 2])


@dataclass
class GameWindow:
    pygame.init()
    game_over: bool = False
    _width: int = Settings.WIDTH
    _height: int = Settings.HEIGHT
    _title: str = Settings.TITLE
    display: Surface = pygame.display.set_mode((_width, _height))
    pygame.display.set_caption(_title)
    game: GameManager = GameManager(display)
    snake: Snake = Snake(display)

    def __post_init__(self):
        self.foods = self.create_foods()

    def main_loop(self) -> None:
        clock = pygame.time.Clock()
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # x change = -10; y change = 0
                        self.snake.change_direction(
                            dx=-Settings.SNAKE_BLOCK_SIZE
                        )
                    elif event.key == pygame.K_RIGHT:
                        # x change = 10; y change = 0
                        self.snake.change_direction(
                            dx=Settings.SNAKE_BLOCK_SIZE
                        )
                    elif event.key == pygame.K_UP:
                        # y change = -10; x change = 0
                        self.snake.change_direction(
                            dy=-Settings.SNAKE_BLOCK_SIZE
                        )
                    elif event.key == pygame.K_DOWN:
                        # y change = 10; x change = 0
                        self.snake.change_direction(
                            dy=Settings.SNAKE_BLOCK_SIZE
                        )
            if self.check_bounds() or self.snake.self_eat():
                self.game_over = True
            if self.check_food():
                self.snake.grow()
                self.game.increase_points()
                self.foods.append(Food(self.display))

            self.snake.draw()
            for food in self.foods:
                food.draw()
            self.game.show_score()
            pygame.display.update()
            clock.tick(Settings.FPS)

    def create_foods(self):
        foods = []
        for i in range(Settings.MAX_FOODS):
            foods.append(Food(self.display))
        return foods

    def check_bounds(self) -> bool:
        x, y = self.snake.get_position()
        if (
            x >= Settings.WIDTH - 1
            or x < 0
            or y >= Settings.HEIGHT - 1
            or y < 0
        ):
            return True
        return False

    def check_food(self) -> bool:
        x_snake, y_snake = self.snake.get_position()
        for i, food in enumerate(self.foods):
            x_food, y_food = food.get_position()
            if x_snake == x_food and y_snake == y_food:
                self.foods.pop(i)
                return True
        return False


def main() -> None:
    window = GameWindow()
    window.main_loop()
    print('Game over. Exiting...')


if __name__ == "__main__":
    main()

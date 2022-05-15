import pygame
import random

# FPS of the game window
FPS = 10
TITLE = 'Snake game by spaut33'
MAX_CHAINS = 32
SNAKE_COLOR = (55, 120, 255)
FOOD_COLOR = (120, 255, 55)
TEXT_COLOR = (200, 200, 200)
BG_COLOR = (0, 0, 0)
WIDTH = 800
HEIGHT = 600
SNAKE_BLOCK_SIZE = 10
SNAKE_SPEED = 10


class Snake:
    def __init__(self, display):
        self.snake_length = 1
        self.max_chains = MAX_CHAINS
        self.color = SNAKE_COLOR
        self.display = display
        self._snake_block_size = SNAKE_BLOCK_SIZE
        self.dx = 0
        self.dy = 0
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.background_color = BG_COLOR
        self.snake_head = (self.x, self.y)
        self.snake_chain = [self.snake_head]

    def change_direction(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy

    def draw(self):
        self.x += self.dx
        self.y += self.dy
        self.chain()
        self.display.fill(self.background_color)
        for x, y in self.snake_chain:
            pygame.draw.rect(self.display, self.color,
                             [x, y, self._snake_block_size, self._snake_block_size])

    def get_position(self):
        return self.x, self.y

    def grow(self):
        self.snake_length += 1

    def chain(self):
        self.snake_head = (self.x, self.y)
        self.snake_chain.append(self.snake_head)
        if len(self.snake_chain) > self.snake_length:
            del self.snake_chain[0]

    def self_eat(self):
        for block in self.snake_chain[:-1]:
            if block == self.snake_head:
                return True


class Food:
    def __init__(self, display):
        self.display = display
        self.color = FOOD_COLOR
        self._food_size = SNAKE_BLOCK_SIZE
        self.x = round(random.randrange(0, WIDTH - self._food_size) // self._food_size) * self._food_size
        self.y = round(random.randrange(0, HEIGHT - self._food_size) // self._food_size) * self._food_size

    def draw(self):
        pygame.draw.rect(self.display, self.color, [self.x, self.y, self._food_size, self._food_size])

    def get_position(self):
        return self.x, self.y


class GameManager:
    def __init__(self, display):
        self.points = 0
        self.display = display

    def increase_points(self):
        self.points += 1

    def show_score(self):
        score_font = pygame.font.SysFont("tahoma", 14)
        value = score_font.render("Score: " + str(self.points), True, TEXT_COLOR)
        self.display.blit(value, [4, 2])


class GameWindow:
    def __init__(self):
        pygame.init()
        self.game_over = False
        self._width = WIDTH
        self._height = HEIGHT
        self._title = TITLE
        self.display = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption(self._title)
        self.game = GameManager(self.display)
        self.snake = Snake(self.display)
        self.food = Food(self.display)

    def main_loop(self):
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

    def check_bounds(self):
        x, y = self.snake.get_position()
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            return True

    def check_food(self):
        x_snake, y_snake = self.snake.get_position()
        x_food, y_food = self.food.get_position()
        if x_snake == x_food and y_snake == y_food:
            return True


def main():
    window = GameWindow()
    window.main_loop()
    print('Game over. Exiting...')


if __name__ == "__main__":
    main()

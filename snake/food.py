"""Class of Food"""
from dataclasses import dataclass
import random

import pygame
from pygame import Surface

from settings import Settings


@dataclass
class Food:
    display: Surface
    lifetime: int = Settings.DEFAULT_LIFETIME
    food_size: int = Settings.SNAKE_BLOCK_SIZE
    color: tuple = Settings.FOOD_COLOR

    def __post_init__(self) -> None:
        self.x = (
            round(
                random.randrange(0, Settings.WIDTH - self.food_size)
                // self.food_size
            )
            * self.food_size
        )
        self.y = (
            round(
                random.randrange(0, Settings.HEIGHT - self.food_size)
                // self.food_size
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

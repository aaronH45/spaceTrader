"""
This module provides game functionality.
"""
from enum import Enum
import random
from existence import Universe

class Difficulty(Enum):
    """ The enum class for difficulty levels """

    EASY = 1
    MEDIUM = 2
    HARD = 3


class Game:
    """ This class creates the game with a universe instance.
    It also creates the front-end environment of the game. """
    def __init__(self, player):
        """ This method instantiates the Game class given a player, returns nothing """
        self.difficulty = player.get_difficulty()
        self.names = ["Hag", "Bethville", "Hipodoodle", "Gangee", "Krat", "Zoobob",
                      "Jimmee", "Frazzle", "Alabala", "Mackadoo"]
        self.player = player
        self.universe = Universe(10)

    def start_game(self):
        """ Starts the game (gives player credits, gives names
        to regions, sets the player's location randomly) """
        index = 0
        random.shuffle(self.names)
        for region in self.universe.get_universe():
            region.name = self.names[index]
            index = index + 1
        self.player.set_location(random.choice(self.universe.get_universe()))

    def get_player(self):
        """ Returns the player of the game """
        return self.player

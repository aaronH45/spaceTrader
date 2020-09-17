"""
This module defines the character.
"""

import math
from ship import Ship


class Character:
    """This class initializes a Character"""

    def __init__(self, name, difficulty, pts, location):
        """Initializes character."""
        self.name = name
        self.difficulty = difficulty
        self.pts = pts
        if difficulty == "Easy":
            self.credit = 1000
        elif difficulty == "Medium":
            self.credit = 500
        elif difficulty == "Hard":
            self.credit = 100
        self.location = location
        self.ship = Ship([], 10, 5, ["Drifting Furdy", 3, 10, 5])

    # Getters
    def get_name(self):
        """Returns name"""
        return self.name

    def get_difficulty(self):
        """Returns difficulty"""
        return self.difficulty

    def get_pilot(self):
        """Returns pilot points"""
        return self.pts[0]

    def get_fighter(self):
        """Returns fighter points"""
        return self.pts[1]

    def get_merchant(self):
        """Returns merchant points"""
        return self.pts[2]

    def get_engineer(self):
        """Returns engineer points"""
        return self.pts[3]

    def get_credit(self):
        """Returns credit"""
        return self.credit

    def get_location(self):
        """Returns location"""
        return self.location

    def get_ship(self):
        """Returns ship"""
        return self.ship

    # Setters
    def set_name(self, name):
        """Sets name"""
        self.name = name

    def set_difficulty(self, difficulty):
        """Sets difficulty"""
        self.difficulty = difficulty

    def set_credit(self, credit):
        """Sets credit"""
        self.credit = credit

    def set_location(self, location):
        """Sets location"""
        self.location = location

    def travel(self, location):
        """Return travel costs"""
        dis = math.sqrt(location.get_distance(self.location))
        if (self.pts[0]) == 0:
            cost = dis
        else:
            cost = dis / self.pts[0]
        return cost

    # Trade functions
    def buy(self, item, region, ship):
        """Subtracts cost from credits, space from cargo
        Returns a string detailing purchase."""
        # Retrieves item buy cost from region market catalog
        buy_cost = region.get_market(self.get_merchant()).get(item.name)[0]
        # Check if buy cost > available credits
        if buy_cost > self.credit:
            return "Not enough credit!"
        # Check if item size > remaining cargo space
        if item.size > (ship.stats[1] - ship.cargo_size):
            return "Not enough space!"
        # Completes purchase
        self.credit -= buy_cost
        ship.add_cargo(item)
        return "Thanks for buying " + item.name + "!"

    def sell(self, item, region, ship):
        """Adds cost to credits, space to cargo
        Returns a string detailing sale"""
        # Retrieves item sell cost from region market catalog
        sell_cost = region.get_market(self.get_merchant()).get(item.name)[1]
        # Check if item is in cargo
        for cargos in ship.cargo:
            if item.name == cargos.name:
                ship.remove_cargo(cargos)
                self.credit += sell_cost
                return "Thanks for selling " + item.name + "!"
        return "You don't own this item!"

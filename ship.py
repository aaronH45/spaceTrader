"""
This module defines the ship.
"""


class Ship:
    """This class initializes a Ship"""

    def __init__(self, cargo, fuel, health, stats):
        """Initializes ship."""
        self.cargo = cargo
        self.fuel = fuel
        self.health = health
        # Ship type, cargo capacity, fuel capacity, and health
        self.stats = stats
        self.value = fuel + health
        self.cargo_size = 0
        for item in cargo:
            self.value += item.get_value()
            self.cargo_size += item.get_size()

    # Getters
    def get_cargo(self):
        """Returns cargo capacity"""
        return self.cargo

    def get_cargo_size(self):
        """Returns Cargo size"""
        return self.cargo_size

    def get_fuel(self):
        """Returns fuel capacity"""
        return self.fuel

    def get_health(self):
        """Returns fighter points"""
        return self.health

    def get_stats(self):
        """Returns ship type, cargo capacity, fuel capacity, and health capacity"""
        return self.stats

    def get_value(self):
        """Returns the total value of the ship"""
        return self.value

    # Setters
    def add_cargo(self, item):
        """Adds item to cargo if possible"""
        if self.cargo_size < self.stats[1]:
            if item in self.cargo:
                index = self.cargo.index(item)
                self.cargo[index].size += 1
            else:
                self.cargo.append(item)
            self.value += item.get_value()
            self.cargo_size += item.get_size()

    def remove_cargo(self, item):
        """Removes item from cargo if possible"""
        if item in self.cargo:
            self.cargo.remove(item)
            self.cargo_size = self.cargo_size - 1

    def set_fuel(self, fuel):
        """Sets fuel capacity"""
        if 0 <= fuel <= self.stats[2]:
            self.fuel = fuel

    def set_health(self, health):
        """Sets health if valid"""
        if 0 <= health <= self.stats[3]:
            self.health = health

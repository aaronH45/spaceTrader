"""This module contains the classes and functions necessary to operate the game"""
from enum import Enum
import math
import random
from ship import Ship


def _generate_name():
    """Generates a random name for region initialization."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    namelist = []
    namelist.extend(random.sample(alphabet, round(random.uniform(3, 10))))

    return "".join(namelist)


def _generate_coords():
    """Generates region coordinates."""
    x_coord = round(random.uniform(-200, 200))
    y_coord = round(random.uniform(-200, 200))
    return (x_coord, y_coord)


def _coords_valid(name, coords, region_list):
    """Returns true if region coordinates are valid."""
    for region in region_list:
        if region.name == name:
            return False
        x_coord, y_coord = coords
        x_radius, y_radius = region.coords
        # if math.sqrt(math.pow(x-xr, 2) + math.pow(y-yr,2)) - (r + rr) <= 5:
        # return False
        if abs(x_coord - x_radius) <= 5 or abs(y_coord - y_radius) <= 5:
            return False
    return True


class TechLevel(Enum):
    """This Enum holds region tech levels."""

    NOMADIC = 1
    AGRICULTURAL = 2
    MEDIEVAL = 3
    RENAISSANCE = 4
    INDUSTRIAL = 5
    MODERN = 6
    STELLAR = 7


class Item:
    """The Item object, may be inherited by others"""

    def __init__(self, name, value, size, tech):
        """Initializes item with name, value, size, and tech level"""
        self.name = name
        self.value = value
        self.size = size
        self.tech = tech

    def __str__(self):
        """Returns description of item"""
        desc = (
            "Item: "
            + str(self.name)
            + " | Value: "
            + str(self.value)
            + " | Size: "
            + str(self.size)
            + " | Tech Level: "
            + str(self.tech)
            + "\n"
        )
        return desc

    def get_name(self):
        """Returns item name"""
        return self.name

    def get_value(self):
        """Returns item value"""
        return self.value

    def get_size(self):
        """Returns item size"""
        return self.size


class Market:
    """The Market object"""

    def __init__(self, tech):
        """Initializes market stock with item names and base item values"""
        self.stock = []
        self.catalog = {}
        self.stock_catalog = {}
        self.last_update = -1
        multiplier = tech.value + random.uniform(-1, 1)
        for item in Universe.item_index.values():
            self.stock_catalog[item.name] = item
            if item.tech <= tech.value:
                self.stock.append(
                    (item.name, round(item.value * multiplier), item.size)
                )

    def __str__(self):
        """Returns a string containing the list of all items and their base values in the market"""
        market_string = ""
        for item in self.stock:
            market_string += str(item) + "; "
        return market_string

    def get_price_catalog(self, merchant_skill):
        """Market Price Calculator, returns market items and prices
        as dictionary of tuples item_name = (buy_price, sell_price, size)"""
        #self.merchant_skill = merchant_skill
        if merchant_skill != self.last_update:
            discount = 1 - (0.4 * (merchant_skill / (merchant_skill + 1)))
            self.catalog = {}
            for item in self.stock:
                self.catalog[item[0]] = (
                    round(item[1] * discount),
                    round(item[1] * 0.6),
                    item[2],
                )
            self.last_update = merchant_skill
        return self.catalog, self.stock_catalog


class Region:
    """The Region object contains name, coordinates, and tech level."""

    def __init__(self, name, coords, tech):
        """This initializes a Region object."""
        self.name = name
        self.coords = coords
        self.tech = tech
        self.market = Market(tech)
        self.merchant_skill = 0

    def __str__(self):
        """Prints Region details in a string."""
        return (
            "Region Coordinates: (%s, %s)" % self.coords
            + " Region Name: "
            + self.name
            + " Tech Level: "
            + self.tech.name
            + "\n    Base Market: "
            + str(self.market)
        )

    def get_distance(self, coords):
        """Returns distance from coordinates to region."""
        x_coord, y_coord = coords.coords
        x_radius, y_radius = self.coords
        return math.sqrt(
            math.pow(x_coord - x_radius, 2) + math.pow(y_coord - y_radius, 2)
        )

    def get_market(self, merchant_skill):
        """Returns current market prices for region."""
        self.merchant_skill = merchant_skill
        return self.market.get_price_catalog(self.merchant_skill)[0]

class Universe:
    """This class holds coordinates between -200 and 200."""

    __instance = None
    regions = []
    item_index = {}
    ship_index = {}
    # To do: Change civ_count to list of civ names, or create alternative init
    def __init__(self, civ_count):
        if Universe.__instance is None:
            Universe.__instance = self
            # Append plain items (name, value, size, tech level) to item_index
            items = [
                ("Art", 14, 1, 1),
                ("Food", 9, 1, 2),
                ("Pet", 50, 1, 2),
                ("Melee Gear", 32, 2, 3),
                ("Music", 31, 1, 4),
                ("Generator", 100, 2, 5),
                ("Nuclear Material", 300, 3, 5),
                ("Solar Panel", 200, 2, 6),
                ("Computer", 500, 2, 6),
                ("Fusion Drive", 1000, 20, 7),
                ("Sanitation Unit", 2000, 40, 7),
            ]
            ships = [
                ["Drifting Furdy", 3, 10, 5],
                ["Spanking Winds", 5, 10, 6],
                ["Jelly Gall", 10, 15, 10],
                ["Blue of the Wind", 15, 17, 15],
                ["Bully of the Water", 20, 12, 20],
            ]
            for item in items:
                Universe.item_index[item[0]] = Item(item[0], item[1], item[2], item[3])
            for ship in ships:
                Universe.ship_index[ship[0]] = Ship([], item[2], item[3], item)
            # Generate regions
            for _count in range(civ_count):
                new_name = _generate_name()
                new_coords = _generate_coords()
                while not _coords_valid(new_name, new_coords, self.regions):
                    new_name = _generate_name()
                    new_coords = _generate_coords()
                new_tech = TechLevel(math.floor(7 * random.random()) + 1)
                new_region = Region(new_name, new_coords, new_tech)
                self.regions.append(new_region)

    def print_regions(self):
        """Prints all regions in Universe"""
        for region in self.regions:
            print(region)

    def get_universe(self):
        """Returns list of all regions in Universe."""
        return self.regions

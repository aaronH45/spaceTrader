"""
This module is for running our Flask application.
"""
from flask import (
    Flask,
    # flash,
    # redirect,
    # url_for,
    session,
    # logging,
    render_template,
    request,
    jsonify,
)
from flask_session import Session

# from wtforms import Form, StringField, IntegerField
from character import Character
from existence import Universe

# from existence import Universe, Region
from game import Game

APP = Flask(__name__)
SESSION_TYPE = "filesystem"
APP.config.from_object(__name__)
Session(APP)


@APP.route("/")
def welcome_screen():
    """This function renders a welcome screen"""
    return render_template("welcome_screen.html")


@APP.route("/newGame", methods=["POST", "GET"])
def new_game():
    """This function starts a new game"""
    return render_template("new_game.html")


@APP.route("/displayGame", methods=["POST", "GET"])
def display_game():
    """This function displays the game"""
    if request.method == "POST":
        form = request.form
        character = Character(
            form.get("Name"),
            form.get("Difficulty"),
            [
                int(form.get("Pilot")),
                int(form.get("Fighter")),
                int(form.get("Merchant")),
                int(form.get("Engineer")),
            ],
            0,
        )

        # market = Market(NOMADIC)
        # priceCatalog = market.get_price_catalog(form.get('Merchant'))
        game = Game(character)
        game.start_game()
        universes = game.universe.get_universe()
        markets = []
        for region in universes:
            markets.append(region.market)
        price_catalog = []
        price_catalog_item = []
        for market in markets:
            # price_catalog.append(market.get_price_catalog(int(form.get('Merchant')))[0])
            # price_catalog_item.append(market.get_price_catalog(int(form.get('Merchant')))[1])
            price_catalog.append(market.get_price_catalog(character.get_merchant())[0])
            price_catalog_item.append(
                market.get_price_catalog(character.get_merchant())[1]
            )
        session["character"] = character
        session["game"] = game
        session["universes"] = universes
        session["price_catalog"] = price_catalog
        session["price_catalog_item"] = price_catalog_item
        return render_template(
            "display_game.html",
            character=session["character"],
            universe=session["universes"],
            price_catalog=session["price_catalog"],
            price_catalog_item=Universe.item_index,
        )
    raise Exception("Cannot display game if request.method is not POST")


def get_region(name):
    """Gets regions in universe"""
    universe = session.get("universes", "not set")
    for region in universe:
        if region.name == name:
            return region
    return None


@APP.route("/travel", methods=["POST"])
def travel():
    """Allows character to travel to various regions"""
    character = session.get("character", "not set")
    location = request.form["location"]
    location = get_region(location)
    fuel = character.travel(location)

    if character.get_ship().get_fuel() > fuel:
        character.get_ship().set_fuel(character.get_ship().get_fuel() - fuel)
        character.set_location(location)
        session["character"] = character
        code = jsonify({"code": 100, "fuel": character.get_ship().get_fuel()})
    else:
        code = jsonify({"code": 101})
    return code


@APP.route("/fuelCost", methods=["POST"])
def fuel_cost():
    """Return fuel cost for travel"""
    character = session.get("character", "not set")
    location = request.form["location"]
    location = get_region(location)
    return jsonify({"code": 100, "fuelCost": character.travel(location)})


@APP.route("/buy", methods=["POST"])
def buy():
    """Allows character to buy items"""
    character = session.get("character", "not set")
    item = request.form["name"]
    region = request.form["region"]
    region = get_region(region)
    item = get_item(item)
    cargo = []
    message = character.buy(item, region, character.get_ship())
    for item in character.get_ship().get_cargo():
        print(item)
        cargo.append(item.name)
    return jsonify(
        {
            "message": message,
            "cargo_size": character.get_ship().get_cargo_size(),
            "credit": character.get_credit(),
            "cargo": cargo,
        }
    )


@APP.route("/sell", methods=["POST"])
def sell():
    """Allows character to sell item"""
    character = session.get("character", "not set")
    item = request.form["name"]
    region = request.form["region"]
    region = get_region(region)
    item = get_item(item)
    cargo = []
    message = character.sell(item, region, character.get_ship())
    for item in character.get_ship().get_cargo():
        print(item)
        cargo.append(item.name)
    return jsonify(
        {
            "message": message,
            "cargo_size": character.get_ship().get_cargo_size(),
            "credit": character.get_credit(),
            "cargo": cargo,
        }
    )


def get_item(name):
    """Returns specified item"""
    item = Universe.item_index[name]
    print(item.name)
    return item


if __name__ == "__main__":
    APP.run(debug=True)

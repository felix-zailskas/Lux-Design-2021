import math, sys
import numpy as np
import logging
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate
from worker import get_worker_action
from city_tiles import get_city_tile_action
from tile_finding import *


logging.basicConfig(filename='game.log', encoding='utf-8', filemode='w', level=logging.INFO)
DIRECTIONS = Constants.DIRECTIONS

CART_OUTPUT_SIZE = 6
CITY_TILE_OUTPUT_SIZE = 4
game_state = None


def agent(observation, configuration):
    global game_state

    ### Do not edit ###
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
        game_state.id = observation.player
    else:
        game_state._update(observation["updates"])
    
    actions = []

    ### AI Code goes down here! ### 
    player = game_state.players[observation.player]
    opponent = game_state.players[(observation.player + 1) % 2]
    width, height = game_state.map.width, game_state.map.height
    resource_tiles = get_resource_tiles(width, height, game_state)
    # we iterate over all our units and do something with them
    for unit in player.units:
        if unit.is_worker() and unit.can_act():
            # do worker logic
            # determine the move to execute
            action = get_worker_action(player, opponent, unit, game_state, resource_tiles)
            if action:
                actions.append(action)

        elif unit.is_cart() and unit.can_act():
            # do cart logic
            pass

    for city in player.cities.items():
        for city_tile in city[1].citytiles:
            if not city_tile.can_act():
                continue
            action = get_city_tile_action(player, opponent, city_tile, game_state, resource_tiles)
            if action:
                actions.append(action)

    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))

    return actions

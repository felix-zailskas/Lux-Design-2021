import math, sys
import numpy as np
import logging
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate


logging.basicConfig(filename='example.log', encoding='utf-8', filemode='w', level=logging.INFO)
logging.info("Logging")
DIRECTIONS = Constants.DIRECTIONS
WORKER_OUTPUT_SIZE = 8
CART_OUTPUT_SIZE = 6
CITY_TILE_OUTPUT_SIZE = 4
game_state = None


def get_resource_tiles(width, height):
    resource_tiles: list[Cell] = []
    for y in range(height):
        for x in range(width):
            cell = game_state.map.get_cell(x, y)
            if cell.has_resource():
                resource_tiles.append(cell)
    return resource_tiles


def get_closest_resource_tile(resource_tiles, player, unit):
    closest_dist = math.inf
    closest_resource_tile = None
    for resource_tile in resource_tiles:
        if resource_tile.resource.type == Constants.RESOURCE_TYPES.COAL and not player.researched_coal(): continue
        if resource_tile.resource.type == Constants.RESOURCE_TYPES.URANIUM and not player.researched_uranium(): continue
        dist = resource_tile.pos.distance_to(unit.pos)
        if dist < closest_dist:
            closest_dist = dist
            closest_resource_tile = resource_tile
    return closest_resource_tile


def get_closest_city_tile(player, unit):
    closest_city_tile = None
    if len(player.cities) > 0:
        closest_dist = math.inf
        for k, city in player.cities.items():
            for city_tile in city.citytiles:
                dist = city_tile.pos.distance_to(unit.pos)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_city_tile = city_tile
    return closest_city_tile


def append_worker_action(unit, worker_action_vector, actions, game_map):
    action_idx = np.argmax(worker_action_vector)
    if action_idx == 0:
        actions.append(unit.move(DIRECTIONS.NORTH))
    if action_idx == 1:
        actions.append(unit.move(DIRECTIONS.EAST))
    if action_idx == 2:
        actions.append(unit.move(DIRECTIONS.SOUTH))
    if action_idx == 3:
        actions.append(unit.move(DIRECTIONS.WEST))
    if action_idx == 4:
        return
    if action_idx == 5:
        actions.append(unit.pillage())
    if action_idx == 6:
        pass
    if action_idx == 7 and unit.can_build(game_map):
        actions.append(unit.build_city())



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
    resource_tiles = get_resource_tiles(width, height)
    # we iterate over all our units and do something with them
    for unit in player.units:
        if unit.is_worker() and unit.can_act():
            # do worker logic
            logging.info("Worker that can act")
            worker_action_vector = np.zeros(WORKER_OUTPUT_SIZE)
            worker_action_vector[0] = 1
            #append_worker_action(unit, worker_action_vector, actions, game_state.map)

            actions.append(unit.move(DIRECTIONS.WEST))
        elif unit.is_cart() and unit.can_act():
            # do cart logic
            pass

    for city in player.cities.items():
        for city_tile in city.city_tiles:
            if city_tile.can_act():
                pass

    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))
    return actions

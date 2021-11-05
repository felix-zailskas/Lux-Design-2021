import math

import numpy as np
import logging
from tile_finding import get_closest_city_tile, get_closest_resource_tile, dist_to_closest_resource, dist_to_closest_city_tile
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS

WORKER_OUTPUT_SIZE = 8
WORKER_INPUT_SIZE = 12


def take_worker_action(player, opponent, unit, game_state, resource_tiles):
    # create input vector
    input_vector = worker_input_vector(player, opponent, unit, game_state, resource_tiles)
    logging.info(f"Input Vector: {input_vector}")
    # TODO: get output from the network
    worker_action_vector = np.random.rand(WORKER_OUTPUT_SIZE)
    # take the action
    return append_worker_action(player, unit, worker_action_vector, game_state.map, resource_tiles)


def worker_input_vector(player, opponent, unit, game_state, resource_tiles):
    input = []
    wood_dist = dist_to_closest_resource(resource_tiles, unit, resource_type=Constants.RESOURCE_TYPES.WOOD)
    coal_dist = dist_to_closest_resource(resource_tiles, unit, resource_type=Constants.RESOURCE_TYPES.COAL)
    uranium_dist = dist_to_closest_resource(resource_tiles, unit, resource_type=Constants.RESOURCE_TYPES.URANIUM)
    friendly_city_dist = dist_to_closest_city_tile(player, unit)
    opponent_city_dist = dist_to_closest_city_tile(opponent, unit)
    game_time = (game_state.turn % 39) / 39
    # distance to wood
    input.append(wood_dist if wood_dist < math.inf else -1)
    # distance to coal
    input.append(coal_dist if coal_dist < math.inf else -1)
    # distance to uranium
    input.append(uranium_dist if uranium_dist < math.inf else -1)
    # distance to friendly city
    input.append(friendly_city_dist if friendly_city_dist < math.inf else -1)
    # distance to opponent city
    input.append(opponent_city_dist if opponent_city_dist < math.inf else -1)
    # day / night cycle
    input.append(game_time)
    # can mine coal
    input.append(1 if player.researched_coal() else 0)
    # can mine uranium
    input.append(1 if player.researched_uranium() else 0)
    # wood fraction of the cargo
    input.append(unit.cargo.wood / GAME_CONSTANTS["PARAMETERS"]["RESOURCE_CAPACITY"]["WORKER"])
    # coal fraction of the cargo
    input.append(unit.cargo.coal / GAME_CONSTANTS["PARAMETERS"]["RESOURCE_CAPACITY"]["WORKER"])
    # uranium fraction of the cargo
    input.append(unit.cargo.uranium / GAME_CONSTANTS["PARAMETERS"]["RESOURCE_CAPACITY"]["WORKER"])
    # cargo space fraction that is free
    input.append(unit.get_cargo_space_left() / GAME_CONSTANTS["PARAMETERS"]["RESOURCE_CAPACITY"]["WORKER"])
    return np.array(input)



def append_worker_action(player, unit, worker_action_vector, game_map, resource_tiles):
    action_idx = np.argmax(worker_action_vector)
    # move toward wood
    if action_idx == 0:
        logging.info(f"Unit {unit.id} of type worker moves toward wood")
        closest_wood_tile = get_closest_resource_tile(resource_tiles, unit, resource_type=Constants.RESOURCE_TYPES.WOOD)
        if closest_wood_tile:
            return unit.move(unit.pos.direction_to(closest_wood_tile.pos))
    # move toward coal
    if action_idx == 1:
        logging.info(f"Unit {unit.id} of type worker moves toward coal")
        closest_coal_tile = get_closest_resource_tile(resource_tiles, unit, resource_type=Constants.RESOURCE_TYPES.COAL)
        if closest_coal_tile:
            return unit.move(unit.pos.direction_to(closest_coal_tile.pos))
    # move toward uranium
    if action_idx == 2:
        logging.info(f"Unit {unit.id} of type worker moves toward uranium")
        closest_uranium_tile = get_closest_resource_tile(resource_tiles, unit, resource_type=Constants.RESOURCE_TYPES.URANIUM)
        if closest_uranium_tile:
            return unit.move(unit.pos.direction_to(closest_uranium_tile.pos))
    # move toward city
    if action_idx == 3:
        logging.info(f"Unit {unit.id} of type worker moves toward city")
        closes_city_tile = get_closest_city_tile(player, unit)
        if closes_city_tile:
            return unit.move(unit.pos.direction_to(closes_city_tile.pos))
    # build city
    if action_idx == 4:
        logging.info(f"Unit {unit.id} of type worker builds city")
        if unit.can_build(game_map):
            return unit.build_city()
    # pillage
    if action_idx == 5:
        logging.info(f"Unit {unit.id} of type worker pillages")
        return unit.pillage()
    # transfer resources to other unit
    if action_idx == 6:
        logging.info(f"Unit {unit.id} of type worker transfers resources")
        # TODO:
        # get id where to transfer to
        closest_unit = get_closest_unit(player, unit)
        if closest_unit is None:
            return None
        # always transfer the most valuable resource first
        if unit.cargo.uranium > 0:
            return unit.transfer(closest_unit.id, Constants.RESOURCE_TYPES.URANIUM, unit.cargo.uranium)
        if unit.cargo.coal > 0:
            return unit.transfer(closest_unit.id, Constants.RESOURCE_TYPES.COAL, unit.cargo.coal)
        if unit.cargo.wood > 0:
            return unit.transfer(closest_unit.id, Constants.RESOURCE_TYPES.WOOD, unit.cargo.wood)
        return None
    # no action
    if action_idx == 7 and unit.can_build(game_map):
        logging.info(f"Unit {unit.id} of type worker takes no action")
        return None
    return None

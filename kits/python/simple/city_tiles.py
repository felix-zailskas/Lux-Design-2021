import numpy as np
import logging

CITY_TILE_OUTPUT_SIZE = 8
CITY_TILE_INPUT_SIZE = 8


def get_city_tile_action(player, opponent, city_tile, game_state, resource_tiles):
    # create input vector
    input_vector = city_tile_input_vector(player, opponent, city_tile, game_state, resource_tiles)
    #logging.info(f"Input Vector: {input_vector}")
    # TODO: get output from the network
    city_tile_action_vector = np.random.rand(CITY_TILE_OUTPUT_SIZE)
    # take the action
    return city_tile_action(city_tile, city_tile_action_vector)


def city_tile_input_vector(player, opponent, city_tile, game_state, resource_tiles):
    input = []
    city = None
    for _city in player.cities.items():
        if _city[1].cityid == city_tile.cityid:
            city = _city[1]
            break

    game_time = (game_state.turn % 39) / 39
    amt_workers_friendly = 0
    amt_carts_friendly = 0
    amt_workers_opponent = 0
    amt_carts_opponent = 0

    for _unit in player.units:
        amt_workers_friendly += 1 if _unit.is_worker() else 0
        amt_carts_friendly += 1 if _unit.is_cart() else 0
    for _unit in opponent.units:
        amt_workers_opponent += 1 if _unit.is_worker() else 0
        amt_carts_opponent += 1 if _unit.is_cart() else 0

    try:
        worker_ratio_friendly = amt_workers_friendly / (amt_carts_friendly + amt_workers_friendly)
    except ZeroDivisionError:
        worker_ratio_friendly = 0
    try:
        worker_ratio_enemy = amt_workers_friendly / amt_workers_opponent
    except ZeroDivisionError:
        worker_ratio_enemy = 2

    # day / night cycle
    input.append(game_time)
    # can mine coal
    input.append(1 if player.researched_coal() else 0)
    # can mine uranium
    input.append(1 if player.researched_uranium() else 0)
    # worker ratio among own units
    input.append(worker_ratio_friendly)
    # worker ratio compared to enemy
    input.append(worker_ratio_enemy)
    # city size
    input.append(len(city.citytiles))
    # city fuel
    input.append(city.fuel)
    # city upkeep
    input.append(city.light_upkeep)
    return np.array(input)


def city_tile_action(city_tile, city_tile_action_vector):
    action_idx = np.argmax(city_tile_action_vector)
    # build a worker
    if action_idx == 0:
        logging.info(f"City Tile {city_tile.cityid} builds a worker")
        return city_tile.build_worker()
    # build a cart
    if action_idx == 1:
        logging.info(f"City Tile {city_tile.cityid} builds a cart")
        return city_tile.build_cart()
    # research
    if action_idx == 2:
        logging.info(f"City Tile {city_tile.cityid} researches")
        return city_tile.research()
    # no action performed
    if action_idx == 3:
        logging.info(f"City Tile {city_tile.cityid} does nothing")
        return None
    return None

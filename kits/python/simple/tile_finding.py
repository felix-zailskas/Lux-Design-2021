from lux.game_map import Cell
import math


def get_resource_tiles(width, height, game_state):
    resource_tiles: list[Cell] = []
    for y in range(height):
        for x in range(width):
            cell = game_state.map.get_cell(x, y)
            if cell.has_resource():
                resource_tiles.append(cell)
    return resource_tiles


def get_closest_resource_tile(resource_tiles, unit, resource_type=None):
    closest_dist = math.inf
    closest_resource_tile = None
    for resource_tile in resource_tiles:
        if resource_type is not None and resource_tile.resource.type != resource_type: continue
        dist = resource_tile.pos.distance_to(unit.pos)
        if dist < closest_dist:
            closest_dist = dist
            closest_resource_tile = resource_tile
    return closest_resource_tile


def dist_to_closest_resource(resource_tiles, unit, resource_type=None):
    closest_dist = math.inf
    for resource_tile in resource_tiles:
        if resource_type is not None and resource_tile.resource.type != resource_type: continue
        dist = resource_tile.pos.distance_to(unit.pos)
        if dist < closest_dist:
            closest_dist = dist
    return closest_dist


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


def dist_to_closest_city_tile(player, unit):
    closest_dist = math.inf
    if len(player.cities) > 0:
        for k, city in player.cities.items():
            for city_tile in city.citytiles:
                dist = city_tile.pos.distance_to(unit.pos)
                if dist < closest_dist:
                    closest_dist = dist
    return closest_dist


def get_closest_unit(player, unit):
    pass

# -*- coding: utf-8 -*-
import textwrap
from src.biosim.geography import Geography
from src.biosim.fauna import Population

"""
This is the Island model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Island:
    geo_types = {'O': 'Ocean', 'S': 'Savannah', 'M': 'Mountain',
                 'J': 'Jungle', 'D': 'Desert'}

    param_keys = ['O', 'S', 'M', 'J', 'D', 'Herbivore', 'Carnivore']

    def __init__(self, island_map):
        self.island_map = island_map
        self.geos = self.list_geo_cells()
        self.check_line_lengths()
        self.check_invalid_character()
        self.check_invalid_boundary()

        self.geo = Geography(self.geos)
        self.geographies = self.geo.create_cells()

        self.pop = Population(self.geos)
        self.population = self.pop.create_cells()

    def list_geo_cells(self):
        geogr = textwrap.dedent(self.island_map).splitlines()
        return [list(row.strip()) for row in geogr]

    def check_line_lengths(self):
        length_count = [len(row) for row in self.geos]
        for i in length_count:
            if i is not length_count[0]:
                raise ValueError('Different line lengths detected')

    def check_invalid_character(self):
        for row in self.geos:
            for letter in row:
                if letter not in self.geo_types.keys():
                    raise ValueError('Invalid character identified')

    def check_invalid_boundary(self):
        for north in self.geos[0]:
            for south in self.geos[-1]:
                if north is not 'O' or south is not 'O':
                    raise ValueError('The boundary is not Ocean')
        for row in self.geos:
            west, east = row[0], row[-1]
            if west is not 'O' or east is not 'O':
                raise ValueError('The boundary is not Ocean')

    def check_param_keys(self, param_key):
        if param_key not in self.param_keys:
            raise ValueError('Parameter type *{}* not '
                             'found'.format(param_key))

    @staticmethod
    def check_param_instance(params):
        if not isinstance(params, dict):
            raise TypeError('params variable must be provided as '
                            'dictionary')

    def set_parameters(self, param_key, params):
        param_key = self.check_param_keys(param_key)
        params = self.check_param_instance(params)
        param_key(self.geos).set_parameters(params)

    def add_population(self, population):
        """[{ "loc": (10, 10),
           "pop": [{"species": "Herbivore", "age": 5, "weight": 20}],
           "loc": (10, 10),
           "pop": [{"species": "Carnivore", "age": 10, "weight": 05}]}]
        """
        pass

    def yearly_cycle(self):
        pass

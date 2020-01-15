# -*- coding: utf-8 -*-
import textwrap
from src.biosim.geography import Ocean, Savannah, Mountain, Jungle, \
    Desert
from src.biosim.fauna import Herbivore, Carnivore

"""
This is the Island model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Island:

    habitable_geos = {'S': Savannah, 'J': Jungle, 'D': Desert}

    fauna_classes = {'Herbivore': Herbivore, 'Carnivore': Carnivore}

    geo_classes = {'O': Ocean, 'S': Savannah, 'M': Mountain,
                   'J': Jungle, 'D': Desert}

    @staticmethod
    def check_dict_instance(argument):
        if not isinstance(argument, dict):
            raise TypeError('Argument *{}* must be provided as '
                            'dictionary'.format(argument))

    @staticmethod
    def check_list_instance(argument):
        if not isinstance(argument, list):
            raise TypeError('Argument *{}* must be provided as '
                            'list'.format(argument))

    def __init__(self, island_map):
        self.island_map = island_map
        self.geos = self.list_geo_cells()
        self.check_line_lengths()
        self.check_invalid_character()
        self.check_invalid_boundary()

        self.cells = self.create_cells()

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
                if letter not in self.geo_classes.keys():
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

    def create_cells(self):
        loc = [(i, j) for i in range(len(self.geos))
               for j in range(len(self.geos[0]))]
        geo = [self.geo_classes[geo]() for j in range(len(self.geos))
               for geo in self.geos[j]]
        return dict(zip(loc, geo))

    def set_parameters(self, param_key, params):
        self.check_dict_instance(params)
        merged_classes = dict(**self.fauna_classes, **self.geo_classes)
        merged_classes[param_key].set_parameters(params)

    def check_coordinates_exists(self, coordinates):
        if coordinates not in self.cells.keys():
            raise ValueError('These *{}* coordinates are not '
                             'found'.format(coordinates))

    def check_habitability(self, coordinates):
        if type(self.cells[coordinates]) not in \
                self.habitable_geos.values():
            raise TypeError('This *{}* area is not '
                            'habitable'.format(coordinates))

    def add_population(self, given_pop):
        self.check_list_instance(given_pop)

        for population in given_pop:
            coordinates = population['loc']
            self.check_coordinates_exists(coordinates)
            self.check_habitability(coordinates)
            geo_object = self.cells[coordinates]

            individuals = []
            for individual in population['pop']:
                species = individual['species']
                age, weight = individual['age'], individual['weight']
                new_individual = \
                    self.fauna_classes[species](age, weight)
                individuals.append(new_individual)
            # geo_object.add_population(individuals)
            for animal in individuals:
                geo_object.population[type(animal)].append(animal)
            
    def yearly_cycle(self):
        for coordinates, geo_object in self.cells.items():
            if type(geo_object) in self.habitable_geos.values():
                geo_object.feed(), geo_object.procreate()
        # self.migrate()
        # self.add_newborns()
        # self.weight_loss(), self.aging(), self.death()
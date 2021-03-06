# -*- coding: utf-8 -*-

"""
This is the fauna pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import pytest
from biosim.simulation import BioSim
import numpy as np
from biosim.fauna import Herbivore, Carnivore
import random as rd

rd.seed(123456)


@pytest.fixture(autouse=True)
def test_check_unknown_parameters():
    """Test method 'check_unknown_parameters()' if it does not
    identifies the given parameter and returns ValueError"""
    with pytest.raises(ValueError):
        Herbivore.check_unknown_parameters(params={'zetaa': 100})
        Carnivore.check_unknown_parameters(params={'muu': 100})


def test_check_known_parameters():
    """Test method 'check_unknown_parameters()' if it identifies the
    given parameter and does not return ValueError"""
    Herbivore.check_unknown_parameters(params={'zeta': 100})
    Carnivore.check_unknown_parameters(params={'mu': 100})


def test_animal_got_old():
    """Test if the method 'get_old()' correctly increases in 1 year a
    specie_object age"""
    island_map = "OOOOO\nOJJJO\nOOOOO"
    ini_pop = [
        {
            "loc": (1, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                    {"species": "Carnivore", "age": 4, "weight": 20}],
        }]
    t, loc = BioSim(island_map, ini_pop, None), (1, 2)
    herb_object = t.island.habitable_cells[loc].population[
        'Herbivore'][0]
    carn_object = t.island.habitable_cells[loc].population[
        'Carnivore'][0]
    herb_age_1 = herb_object.age
    carn_age_1 = carn_object.age
    herb_object.get_old()
    carn_object.get_old()
    herb_age_2 = herb_object.age
    carn_age_2 = carn_object.age
    assert herb_age_2 is (herb_age_1 + 1)
    assert carn_age_2 is (carn_age_1 + 1)


def test_calculate_fitness_and_formula():
    """Test if the method 'calculate_fitness()' correctly communicates to
    the method 'fit_formula()' and returns the correct fitness of the
    animal (pop_object)'"""

    herbivore = Herbivore(10, 20)
    carnivore = Carnivore(15, 30)
    assert pytest.approx(herbivore.calculate_fitness(herbivore.age,
                                                     herbivore.weight,
                                                     herbivore.parameters),
                         0.7292)
    assert pytest.approx(carnivore.calculate_fitness(carnivore.age,
                                                     carnivore.weight,
                                                     carnivore.parameters),
                         0.999969)


def test_check__phi_borders():
    """Test if method 'check__phi_borders()' verifies the _phy
    conditions '0 <= _phi <= 1' and returns an ValueError if  not
    satisfied"""
    with pytest.raises(ValueError):
        Herbivore(1, 50).check__phi_borders(-0.9999)
        Carnivore(1, 50).check__phi_borders(-0.9999)
        Herbivore(1, 50).check__phi_borders(1.0001)
        Carnivore(1, 50).check__phi_borders(1.0001)


def test_create_animal():
    """"""
    h = Herbivore()
    assert h.age == 0


def test_herbivore_params_keys():
    """ Tests that the given parameters are in the list of herbivor
    parameters"""
    keys_list = ['w_birth', 'sigma_birth', 'beta', 'eta', 'a_half',
                 'phi_age', 'w_half', 'phi_weight', 'mu', 'lambda',
                 'gamma', 'zeta', 'xi', 'omega', 'F', 'DeltaPhiMax']
    h = Herbivore()
    assert [key in h.parameters for key in keys_list]


def test_animal_non_neagtive_weight():
    """
    test if animal age is  non-negative
    """
    h = Herbivore()
    c = Carnivore()
    assert h.weight >= 0
    assert c.weight >= 0


def test_animal_aging():
    """
    test every year animal age updates
    """
    animal = Herbivore(10, 50)
    before_age = animal.age
    animal.get_old()
    assert animal.age == before_age + 1


def test_animal_weight_loss():
    """
    Test if animal looses weight
    """
    animal = Herbivore(10, 50)
    before_weight = animal.weight
    animal.lose_weight()
    assert before_weight > animal.weight


def test_fitness_range():
    """
    test fitness value is between 0 and 1
    """
    herb = Herbivore(np.random.randint(0, 100), np.random.randint(0, 100))
    carn = Carnivore(np.random.randint(0, 100), np.random.randint(0, 100))
    assert 1 >= herb.fitness >= 0
    assert 1 >= carn.fitness >= 0


def test_fitness_update():
    """
    test fitness is updated when weight is changed
    """
    animal = Herbivore(10, 50)
    before_fitness = animal.fitness
    animal.lose_weight()
    assert animal.fitness != before_fitness


def test_animal_death():
    """
    test that animal dies when fitness is 0 or with
    certain probability omega(1 - fitness)
    """
    animal = Herbivore(10, 50)
    animal.fitness = 0
    assert animal.will_die() is True


def test_animal_migration_chances():
    """
    test the probability of migration is zero if
    fitness is zero
    """
    animal = Herbivore(10, 50)
    animal.fitness = 0
    assert not animal.will_migrate()


def test__animal_birth_probability():
    """
    1. Test no birth if single herbivore or carnivore
    2. Test no birth if weight of herbivore or
    carnivore is less than output of following
    condition:
        xi(w_birth + sigma_birth)
    """
    animal = Herbivore(20, 50)
    assert not animal.birth(1)

    animal = Carnivore(10, 50)
    animal.weight = 5
    assert not animal.birth(200)


def test_update_weight_after_birth():
    """
    test that the weight of the mother is
    reduced by xi times the weight of the
    baby after reproduction
    """
    animal = Herbivore(20, 40)
    weight_before_birth = animal.weight
    baby_weight = 10
    animal.update_weight_after_birth(baby_weight)
    assert animal.weight < weight_before_birth


def test_carnivore_kill(mocker):
    """
    Test that carnivore kills herbivore if
        1. carnivore fitness is greater than
        herbivore fitness
        2. the difference between carnivore
        fitness and herbivore fitness divided
        by DeltaPhiMax parameter is greater
        than random value.
    """
    mocker.patch('numpy.random.random', return_value=0.05)
    herbivore = Herbivore()
    carnivore = Carnivore()
    herbivore.fitness = 0.3
    carnivore.fitness = 0.9
    assert carnivore.will_kill(herbivore.fitness)


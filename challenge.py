#!/usr/bin/env python3.6

import random
import pytest

class FairDie:
    def __init__(self, sides: int):
        self.sides = sides

    def roll(self) -> int:
        return random.randrange(self.sides) + 1

class LoadedDie:
    def __init__(self, sides: int, weighted_side: int, weight: int):
        self.sides = sides
        self.weighted_side = weighted_side
        self.weight = weight

    def roll(self) -> int:
        # treat weight as additional ints that will map to the same side
        roll = random.randrange(1, self.weight + self.sides)

        # map to weighted_side
        if roll <= self.weight:
            return self.weighted_side

        # remove weight if weighted side did not get rolled
        roll -= self.weight

        # if roll is above weighted_side, add 1 to skip weighted_side
        if roll >= self.weighted_side:
            roll += 1

        return roll

def test_loaded_die() -> None:
    # define test case tuples (sides, weighted_side, weight)
    test_cases = [(2, 2, 1), (2, 2, 5), (6, 1, 3), (6, 6, 4), (5, 3, 1)]

    for sides, weighted_side, weight in test_cases:
        print("Sides: {}  Weighted Side: {}  Weight: {}".format(
            sides, weighted_side, weight
        ))
        die = LoadedDie(sides, weighted_side, weight)

        result_distribution = [0] * sides

        # obtain a sampled distribution of results
        n_trials = 10000
        for _ in range(n_trials):
            result_distribution[die.roll()-1] += 1

        margin = 0.1  # % margin to match expectation within [0 ... 1]

        # expectation for non_weighted sides
        expected_non_weighted = n_trials / (sides + weight - 1)
        # expectation for weighted side
        expected_weighted = expected_non_weighted * weight

        print("Results: ", result_distribution)
        # for every result
        for i, a_res in enumerate(result_distribution):
            # decide which expectation to use
            expected = expected_non_weighted
            if i == weighted_side - 1:
                expected = expected_weighted

            # check if the expectation is true (within the margin)
            assert abs(a_res - expected) < expected * margin

def test_fair_die() -> None:
    # define test cases (side argument)
    test_cases = [2, 4, 7]

    for sides in test_cases:
        print("Sides: {}".format(sides))
        die = FairDie(sides)

        result_distribution = [0] * sides

        # obtain a sampled distribution of results
        n_trials = 10000
        for _ in range(n_trials):
            result_distribution[die.roll()-1] += 1

        margin = 0.1  # % margin to match expectation within [0 ... 1]

        # expectation for non_weighted sides
        expected = n_trials / sides

        print("Results: ", result_distribution)
        # for every result
        for i, a_res in enumerate(result_distribution):

            # check if the expectation is true (within the margin)
            assert abs(a_res - expected) < expected * margin

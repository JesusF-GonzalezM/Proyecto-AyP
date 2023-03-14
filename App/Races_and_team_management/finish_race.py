import random


# orders the list in a random order
def randomize_list(drivers_list):
    random.shuffle(drivers_list)
    return drivers_list


def set_drivers_and_constructors_score(drivers, constructors):
    drivers[0].score = 25
    drivers[1].score = 18
    drivers[2].score = 15
    drivers[3].score = 12
    drivers[4].score = 10
    drivers[5].score = 8
    drivers[6].score = 6
    drivers[7].score = 4
    drivers[8].score = 2
    drivers[9].score = 1

    for constructor in constructors:
        constructor.set_score(drivers)


def get_winning_constructor(constructors):
    winning_constructor = constructors[0]
    for constructor in constructors:
        if constructor.score > winning_constructor.score:
            winning_constructor = constructor
    return winning_constructor


def reset_scores(drivers, constructors):
    for driver in drivers:
        driver.score = 0
    for constructor in constructors:
        constructor.score = 0

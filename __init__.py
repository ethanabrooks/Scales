from copy import copy
from itertools import cycle

__author__ = 'Ethan'
from random import *

__author__ = 'Ethan'

# {0: 'A', 1: 'Bb', 2: 'B', 3: 'C', 4: 'Dd', 5: 'D', 6: 'Eb', 7: 'E', 8: 'F', 9: 'Gb', 10: 'G', 11: 'Ab'}
notes_flat = {entry[0]: entry[1] for entry in zip(range(12), "A Bb B C Dd D Eb E F Gb G Ab".split())}
# {0: 'A', 1: 'A#', 2: 'B', 3: 'C', 4: 'C#', 5: 'D', 6: 'D#', 7: 'E', 8: 'F', 9: 'F#', 10: 'G', 11: 'G#'}
notes_sharp = {entry[0]: entry[1] for entry in zip(range(12), "A A# B C C# D D# E F F# G G#".split())}

scales = (
    [0, 2, 4, 5, 7, 9, 11],
    [0, 1, 4, 5, 8, 9],
    [0, 1, 3, 4, 6, 7, 9, 10],
    [0, 2, 4, 6, 8, 10],
    [0, 2, 3, 5, 7, 8, 11],
    [0, 2, 4, 5, 7, 8, 11],
    [0, 2, 4, 6, 7, 9, 10],
    [0, 2, 4, 5, 7, 9, 11]
)

# index of scales and names
name_notes = {entry[0]: entry[1] for entry in zip('oct wt hmi hma ac dia'.split(), scales)}


def intervals(scale):
    """
    :param scale:
    :return: list of intervals, numbered by half steps
    """
    scale = list(scale)
    return [next - prev for next, prev in zip(wrapped_scale, scale)]


def jumps(scale):
    """
    :param scale:
    :return: True if all intervals less than minor third
    """
    return any([interval > 3 for interval in intervals(scale)])


def aug_2nd_specs(scale):
    """
    :param scale:
    :return: True if all minor thirds have a half step on left and right
    """
    intervals_ = intervals(scale)
    for i, interval in enumerate(intervals_):
        if interval == 3:
            next_index = i + 1 % len(scale)
            if intervals_[i - 1] != 1 \
                    or intervals_[next_index] != 1:
                return False
    return True


def min_2nd_specs(scale):
    """
    :param scale:
    :return: True if no adjacent half steps
    """
    intervals_ = intervals(scale)
    for i, interval in enumerate(intervals_):
        if intervals_[i - 1] == 1 and interval == 1:
            return False
    return True


def meets_specs(scale):
    if not jumps(scale):
        if aug_2nd_specs(scale):
            if min_2nd_specs(scale):
                return True
    return False


def sharp(scale, note):
    scale[note] += 1
    return scale


def flat(scale, note):
    scale[note] -= 1
    return scale


def split(scale, note):
    scale.append(scale[note] + 1)
    return flat(scale, note)


def merge(scale, note):
    scale.sort()
    del scale[note - 1]
    return sharp(scale, note - 1)


def fix_up(scale):
    scale.sort()
    root = randrange(len(scale))
    return scale[root:] + scale[:root]


def get_next_scale(scale):
    mods = [sharp, flat, split, merge]
    shuffle(mods)
    while True:
        note_to_modify = choice(range(len(scale)))
        for modification in mods:
            scale_copy = copy(scale)
            new_scale = set(modification(scale_copy, note_to_modify))
            if meets_specs(new_scale):
                break
    return fix_up(new_scale)


def display_notes_sharp(scale):
    return ' '.join(notes_sharp[note] for note in scale)


def display_notes_flat(scale):
    return ' '.join(notes_sharp[note] for note in scale)


def valid_display_type():
    pass


def get_valid_input(prompt, validation, prompt_on_fail=None, exception=Exception):
    """
    :param prompt: initial prompt for user input
    :param validation: dict of inputs with corresponding return values
    :return: value in index corresponding with input
    """
    if prompt_on_fail is None:
        prompt_on_fail = prompt
    print(prompt, end="")
    while True:
        user_input = input()
        try:
            return validation(user_input)
        except exception:
            print(prompt_on_fail, end="")

def display_validation(user_input):
    if user_input == 's':
        return display_notes_sharp
    elif user_input == 'f':
        return display_notes_flat
    else:
        raise ValueError

NUM_NOTES = 12
len_1st_scale = 8 # get_valid_input(
#     'How many notes would you like in your first scale: ',
#     int,
#     'Please enter a number: ',
#     ValueError
# )
display = display_notes_flat # get_valid_input(
#     'Display notes in sharp or flat (type [s|f]: ',
#     display_validation,
#     'Please enter either "s" or "f": ',
#     ValueError
# )
scale = fix_up(sample(range(NUM_NOTES), len_1st_scale))
while True:
    print(display(scale))
    # input('Press Enter for next scale...')
    scale = get_next_scale(scale)

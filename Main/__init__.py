__author__ = 'Ethan'
from random import *

__author__ = 'Ethan'

notes_flat = {entry[0]: entry[1] for entry in zip(range(12), "A Bb B C Dd D Eb E F Gb G Ab".split())}
# <= {0: 'A', 1: 'Bb', 2: 'B', 3: 'C', 4: 'Dd', 5: 'D', 6: 'Eb', 7: 'E', 8: 'F', 9: 'Gb', 10: 'G', 11: 'Ab'}
notes_sharp = {entry[0]: entry[1] for entry in zip(range(12), "A A# B C C# D D# E F F# G G#".split())}
# <= {0: 'A', 1: 'A#', 2: 'B', 3: 'C', 4: 'C#', 5: 'D', 6: 'D#', 7: 'E', 8: 'F', 9: 'F#', 10: 'G', 11: 'G#'}


named_scales = (
    [0, 2, 4, 5, 7, 9, 11],
    [0, 1, 4, 5, 8, 9],
    [0, 1, 3, 4, 6, 7, 9, 10],
    [0, 2, 4, 6, 8, 10],
    [0, 2, 3, 5, 7, 8, 11],
    [0, 2, 4, 5, 7, 8, 11],
    [0, 2, 4, 6, 7, 9, 10],
    [0, 2, 4, 5, 7, 9, 11]
)

scale_namer = {entry[0]: entry[1] for entry in zip('oct wt hmi hma ac dia'.split(), named_scales)}


def match(list1, list2):
    return all([entry[0] == entry[1] for entry in zip(list1, list2)])


def trizip(list1, list2, list3):
    if not (list1 and list2 and list3):
        return []
    return [(list1[0], list2[0], list3[0])] + trizip(list1[1:], list2[1:], list3[1:])


def compare(list1, list2):
    """
    Identifies integers in one list that are not in the other and vice versa.
    :param list1: [integers] -- probably notes
    :param list2: [integers] -- probably notes
    :return: 2-tuple of lists of numbers that list1 possesses that list2 does not possess and vice versa, respectively.
    """
    not_in_list1 = list2
    not_in_list2 = []
    for integer in list1:
        if integer in list2:
            not_in_list1.remove(integer)
        else:
            not_in_list2.append(integer)
    return not_in_list2, not_in_list1


def remove_duplicates(list):
    one_each = []
    for entry in list:
        if entry not in one_each:
            one_each.append(entry)
    return one_each


def intervals(list):
    adjacents = zip(list, list[1:])
    return [(entry[1] - entry[0]) % 12 for entry in adjacents] + [(list[0] - list[-1]) % 12]


def jumps(list):
    return any([interval > 3 for interval in intervals(list)])


def aug_2nd_specs(list):
    triplets = trizip(intervals(list), intervals(list)[1:], intervals(list)[2:])
    aug_2nds = [tri for tri in triplets if tri[1] == 3]
    return all([tri[0] == 1 and tri[2] == 1 for tri in aug_2nds])


def min_2nd_specs(list):
    adjacent_intervals = [i for i in zip(intervals(list), intervals(list)[1:])]
    return not any([interval[0] == 1 for interval in adjacent_intervals if interval[1] == 1])


def meets_specs(list):
    if not jumps(list):
        if aug_2nd_specs(list):
            if min_2nd_specs(list):
                return True
    return False


def get_type(scale_notes):
    for type in scale_namer:
        if match(scale_notes, type):
            return type


class Scale():
    def __init__(self, root, notes):
        self.root = root
        self.notes = [root] + sorted([note for note in notes if note > root]) + sorted(
            [note for note in notes if note < root])
        self.type = get_type(notes)
        self.intervals = intervals(self.notes)
        assert meets_specs(self.notes)

    def copy(self):
        return Scale(self.root, self.notes)


    def sharp(self, note_index):
        """

        :param note_index:
        :return:
        """
        mod_scale = [note for note in self.notes]
        mod_scale[note_index] = self.notes[note_index] + 1
        return mod_scale

    def flat(self, note_index):
        mod_scale = [note for note in self.notes]
        mod_scale[note_index] = self.notes[note_index] - 1
        return mod_scale

    def split(self, note_index):
        mod_scale = self.sharp(note_index)
        mod_scale.insert(note_index, self.notes[note_index] - 1)
        return mod_scale

    def merge(self, note_index):
        mod_scale = self.flat((note_index + 1) % len(self.notes))
        mod_scale.remove(mod_scale[note_index])
        return mod_scale

    def get_next_scale(self):
        note_to_modify = randint(0, len(self.notes) - 1)
        mods = [self.sharp, self.flat, self.split, self.merge]
        while True:
            modification = choice(mods)
            mod_scale = remove_duplicates([note % 12 for note in modification(note_to_modify)])
            if meets_specs(mod_scale):
                break
            ints = intervals(mod_scale)
            if mods:
                mods.remove(modification)
            if not mods:
                mods = [self.sharp, self.flat, self.split, self.merge]
                note_to_modify = randint(0, len(self.notes) - 1)
        ints = intervals(mod_scale)
        assert meets_specs(mod_scale)
        new_root = choice(mod_scale)
        new_scale = Scale(new_root, mod_scale)
        return new_scale


    def display_notes_sharp(self):
        return ' '.join([notes_sharp[note] for note in self.notes])


    def display_notes_flat(self):
        return ' '.join([notes_flat[note] for note in self.notes])


def test():
    scale = Scale(root=7, notes=[0, 2, 4, 5, 7, 9, 11])
    assert scale.notes == [7, 9, 11, 0, 2, 4, 5]
    assert scale.display_notes_flat() == "E Gb Ab A B Dd D"
    assert scale.display_notes_sharp() == "E F# G# A B C# D"
    randlist = [randint for i in range(12)]
    assert match(randlist, randlist) == True
    assert match([0] + randlist, [1] + randlist) == False
    assert match(randlist + [0], randlist + [1]) == False
    next_scale = scale.get_next_scale()
    assert aug_2nd_specs([0, 1, 3, 4, 7, 8, 9]) == True
    assert aug_2nd_specs([0, 1, 4, 7, 8, 9]) == False
    assert aug_2nd_specs([0, 3, 4, 7, 8, 11]) == True
    assert aug_2nd_specs([0, 1, 4, 5, 8]) == False
    assert min_2nd_specs([0, 1, 9, 10]) == True
    assert min_2nd_specs([0, 1, 9, 10, 11]) == False

    print(next_scale.notes)
    print(next_scale.display_notes_flat())


test()


def initialize():
    current_type = choice(named_scales)
    random_number = randint(0, 12)
    current_notes = [(note + random_number) % 12 for note in current_type]
    ints = intervals(current_notes)
    assert meets_specs(current_notes)
    return [Scale(current_notes[0], current_notes)]


current_scale = initialize()
current_scale[0].get_next_scale()

# initialize()


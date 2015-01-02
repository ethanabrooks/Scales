__author__ = 'Ethan'
from random import *
import audioop

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


def duplicates(list):
    adjacents = zip(list, list[1:])
    return any([entry[0] == entry[1] for entry in adjacents]) or list[0] == list[-1]


def jumps(list):
    adjacents = zip(list, list[1:])
    intervals = [(entry[1] - entry[0]) % 12 for entry in adjacents] + [list[0] - list[-1] % 12]
    return any([(entry[1] - entry[0]) % 12 > 3 for entry in adjacents]) or (list[0] - list[-1]) % 12 > 3


def meets_specs(list):
    if not duplicates(list):
        if not jumps(list):
            return True
    return False


def get_type(scale_notes):
    for type in scale_namer:
        if match(scale_notes, type):
            return type


class Scale():
    def __init__(self, root, notes):
        self.root = root
        self.notes = [root] + [note for note in notes if note > root] + [note for note in notes if note < root]
        # self.type = get_type(notes)

    def copy(self):
        return Scale(self.root, self.notes)


    def test(self):
        """

        :return:
        """
        assert not duplicates(self.notes)
        assert not jumps(self.notes)


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
            mod_scale = [note % 12 for note in modification(note_to_modify)]
            if meets_specs(mod_scale):
                break
            if mods:
                mods.remove(modification)
            if not mods:
                mods = [self.sharp, self.flat, self.split, self.merge]
        new_root = choice(mod_scale)
        new_scale = Scale(new_root, mod_scale)
        return new_scale


    def display_notes_sharp(self):
        return ' '.join([notes_sharp[note] for note in self.notes])


    def display_notes_flat(self):
        return ' '.join([notes_flat[note] for note in self.notes])


def test():
    test_scale = Scale(root=7, notes=[0, 2, 4, 5, 7, 9, 11])
    test_scales = [test_scale]
    NUM_TO_ADD = 10
    for num in range(NUM_TO_ADD):
        scale = test_scales[-1].copy()
        for rep in range(randint(0, 10)):
            scale = scale.get_next_scale()
        test_scales.append(scale)
    for scale in test_scales:
        assert scale.notes == [7, 9, 11, 0, 2, 4, 5]
        assert scale.display_notes_flat() == "E Gb Ab A B Dd D"
        # assert scale.display_notes_sharp() == "E F# G# A B C# D"
        # randlist = [randint for i in range(12)]
        # assert match(randlist, randlist) == True
        # assert match([0] + randlist, [1] + randlist) == False
        # assert match(randlist + [0], randlist + [1]) == False
        # next_scale = scale.get_next_scale()
        # print(next_scale.notes)
        # print(next_scale.display_notes_flat())


current_type = choice(named_scales)
current_notes = [(note + randint(0, 12)) % 12 for note in current_type]
current_scale = [Scale(current_notes[0], current_notes)]


print((next_scale()).display_notes_flat())
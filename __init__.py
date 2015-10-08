__author__ = 'Ethan'
from random import *

__author__ = 'Ethan'

# {0: 'A', 1: 'Bb', 2: 'B', 3: 'C', 4: 'Dd', 5: 'D', 6: 'Eb', 7: 'E', 8: 'F', 9: 'Gb', 10: 'G', 11: 'Ab'}
notes_flat = {entry[0]: entry[1] for entry in zip(range(12), "A Bb B C Dd D Eb E F Gb G Ab".split())}
# {0: 'A', 1: 'A#', 2: 'B', 3: 'C', 4: 'C#', 5: 'D', 6: 'D#', 7: 'E', 8: 'F', 9: 'F#', 10: 'G', 11: 'G#'}
notes_sharp = {entry[0]: entry[1] for entry in zip(range(12), "A A# B C C# D D# E F F# G G#".split())}

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

# index of scales and names
scale_namer = {entry[0]: entry[1] for entry in zip('oct wt hmi hma ac dia'.split(), named_scales)}


def intervals(scale):
    '''
    :param scale:
    :return: list of intervals, numbered by half steps
    '''
    return [next - prev for next, prev in zip(scale[1:], scale[:-2])]


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
            if intervals_[i - 1] != 1 or intervals_[i + 1] != 1:
                return False
    return True


def min_2nd_specs(scale):
    """
    :param scale:
    :return:
    """
    intervals_ = intervals(scale)
    for i, interval in enumerate(intervals_):
        if interval == 1 and intervals_[i + 1] == 1:
            return False
    return True

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
        return ' '.join([notes_sharp[note] for note in self.notes] + [notes_sharp[self.notes[0]]])


    def display_notes_flat(self):
        return ' '.join([notes_flat[note] for note in self.notes] + [notes_flat[self.notes[0]]])


def test():
    scale1 = Scale(root=7, notes=[0, 2, 4, 5, 7, 9, 11])
    scale2 = Scale(root=9, notes=[0, 2, 4, 5, 7, 9, 11])
    assert scale1.notes == [7, 9, 11, 0, 2, 4, 5]
    assert scale1.display_notes_flat() == "E Gb Ab A B Dd D E"
    assert scale1.display_notes_flat() == "E Gb Ab A B Dd D E"
    assert scale2.display_notes_sharp() == "F# G# A B C# D E F#"
    assert scale2.display_notes_flat() == "Gb Ab A B Dd D E Gb"
    ints = intervals([0, 1, 3, 4, 7, 8, 9])
    assert aug_2nd_specs([0, 1, 3, 4, 7, 8, 9]) == True
    ints = intervals([0, 1, 4, 7, 8, 9])
    assert aug_2nd_specs([0, 1, 4, 7, 8, 9]) == False
    ints = intervals([0, 3, 4, 7, 8, 9])
    assert aug_2nd_specs([0, 3, 4, 7, 8, 9]) == False
    ints = intervals([0, 3, 4, 7, 8, 10])
    assert aug_2nd_specs([0, 3, 4, 7, 8, 10]) == False
    ints = intervals([0, 3, 4, 7, 8, 11])
    assert aug_2nd_specs([0, 3, 4, 7, 8, 11]) == True
    ints = intervals([0, 1, 4, 5, 8])
    assert aug_2nd_specs([0, 1, 4, 5, 8]) == False
    ints = intervals([0, 1, 9, 10])
    assert min_2nd_specs([0, 1, 9, 10]) == True
    ints = intervals([0, 1, 9, 10, 11])
    assert min_2nd_specs([0, 1, 9, 10, 11]) == False
    ints = intervals([2, 3, 4, 7, 8, 10, 11])
    assert min_2nd_specs([2, 3, 4, 7, 8, 10, 11]) == False
    randlist = [randint for i in range(12)]
    assert match(randlist, randlist) == True
    assert match([0] + randlist, [1] + randlist) == False
    assert match(randlist + [0], randlist + [1]) == False
    next_scale = scale1.get_next_scale()

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
while True:
    pause = input('Press Enter for next scale...')
    current_scale[0].get_next_scale()


def next_scale(*args):
    current_scale.append(current_scale[0].get_next_scale())
    del current_scale[0]
    scale_flat.set(current_scale[0].display_notes_flat())
    scale_sharp.set(current_scale[0].display_notes_sharp())
    string_ints = map(str, current_scale[0].intervals)
    ints.set('  '.join(string_ints))


# root = Tk()
# root.title("Feet to Meters")

# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# mainframe.columnconfigure(0, weight=1)
# mainframe.rowconfigure(0, weight=1)

# scale_flat = StringVar()
# scale_sharp = StringVar()
# ints = StringVar()

# ttk.Button(mainframe, text="Next Scale", command=next_scale).grid(column=0, row=0, sticky=W)
# ttk.Label(mainframe, textvariable=scale_flat).grid(column=0, row=1, sticky=(W, E))
# ttk.Label(mainframe, textvariable=scale_sharp).grid(column=0, row=2, sticky=(W, E))
# ttk.Label(mainframe, text="Intervals:").grid(column=0, row=3, sticky=(W))
# ttk.Label(mainframe, textvariable=ints).grid(column=0, row=4, sticky=(W, E))


# for child in mainframe.winfo_children():
# child.grid_configure(padx=5, pady=5)

# root.bind('<Return>', next_scale)

# root.mainloop()


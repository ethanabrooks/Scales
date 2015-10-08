__author__ = 'Ethan'


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
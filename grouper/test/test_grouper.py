"""
test code for grouper class

(run with pytest or maybe nose)

"""


from grouper import Grouping

from operator import itemgetter

# example data from the mailing list.
student_school_list = [('Fred', 'SchoolA'),
                       ('Bob', 'SchoolB'),
                       ('Mary', 'SchoolA'),
                       ('Jane', 'SchoolB'),
                       ('Nancy', 'SchoolC'),
                       ]

student_school_dict = {'SchoolA': ['Fred', 'Mary'],
                       'SchoolB': ['Bob', 'Jane'],
                       'SchoolC': ['Nancy']
                       }


def test_init_empty():
    gr = Grouping()
    assert len(gr) == 0


def test_add_one_item():
    gr = Grouping()

    gr['key'] = 'value'

    assert len(gr) == 1
    assert gr['key'] == ['value']


def test_example_loop():
    gr = Grouping()

    for student, school in student_school_list:
        gr[school] = student

    assert len(gr) == 3

    assert gr['SchoolA'] == ['Fred', 'Mary']
    assert gr['SchoolB'] == ['Bob', 'Jane']
    assert gr['SchoolC'] == ['Nancy']


def test_constructor_list():
    """
    Trying to be as similar to the dict constructor as possible:

    We can use pass an iterable of (key, value) tuples, the keys
    will be what is grouped by, and the values will be in the groups.
    """
    gr = Grouping(((item[1], item[0]) for item in student_school_list))

    assert len(gr) == 3

    assert gr['SchoolA'] == ['Fred', 'Mary']
    assert gr['SchoolB'] == ['Bob', 'Jane']
    assert gr['SchoolC'] == ['Nancy']


def test_constructor_dict():
    """
    Trying to be as similar to the dict constructor as possible:

    You can contruct with a Mapping that already has groups
    """
    gr = Grouping(student_school_dict)

    assert len(gr) == 3

    assert gr['SchoolA'] == ['Fred', 'Mary']
    assert gr['SchoolB'] == ['Bob', 'Jane']
    assert gr['SchoolC'] == ['Nancy']


def test_simple_sequence_example():
    """
    This was a example / use case in Michael Selik's PEP
    """
    gr = Grouping(((c.casefold(), c) for c in 'AbBa'))

    assert gr == {'a': ['A', 'a'],
                  'b': ['b', 'B']}


def test_most_common():
    gr = Grouping(((c.casefold(), c) for c in 'AbBaAAbCccDe'))
    common = gr.most_common()
    assert len(common) == len(gr)

    common = gr.most_common(2)

    print(common)
    assert len(common) == 2
    assert common == [('a', ['A', 'a', 'A', 'A']), ('b', ['b', 'B', 'b'])]


# you can specify a key_fun and or value_fun instead:
# some examples from the PEP:
def test_names_by_first_initial():
    names = ["Fred", "Bob", "Frank", "Mary", "Billy"]
    gr = Grouping(names, key_fun=itemgetter(0))

    assert gr == {'F': ['Fred', 'Frank'], 'B': ['Bob', 'Billy'], 'M': ['Mary']}


def test_only_specify_value():
    """
    last names by first initial
    """
    data = [("Seattle", "Cleveland", "Barker"),
            ("Cleveland", "Oakland", "Jones"),
            ("Cleveland", "San Jose", "Miller"),
            ("Seattle", "Boston", "Cooper"),
            ("San Francisco", "Atlanta", "Barker"),
            ]

    gr = Grouping(data, value_fun=itemgetter(2))

    print(gr)
    assert gr == {'Seattle': ['Barker', 'Cooper'],
                  'Cleveland': ['Jones', 'Miller'],
                  'San Francisco': ['Barker']}

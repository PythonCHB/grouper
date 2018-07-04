#!/usr/bin/env python3

"""
Demo of processing "trigrams" from Dave Thomas' Coding Kata site:

http://codekata.com/kata/kata14-tom-swift-under-the-milkwood/

This is only addressing the part of the problem of building up the trigrams.the

This is showing various ways of doing it with the Grouping object.
"""

from grouper import Grouping
from operator import itemgetter

words = "I wish I may I wish I might".split()

# using setdeafult with a regular dict:

trigrams = {}
for i in range(len(words) - 2):
    pair = tuple(words[i:i + 2])
    follower = words[i + 2]
    trigrams.setdefault(pair, []).append(follower)

print(trigrams)

# using a Grouping with a regular loop:

trigrams = Grouping()
for i in range(len(words) - 2):
    pair = tuple(words[i:i + 2])
    follower = words[i + 2]
    trigrams[pair] = follower

print(trigrams)

# using a Grouping with zip

trigrams = Grouping()
for w1, w2, w3 in zip(words[:], words[1:], words[2:]):
    trigrams[(w1, w2)] = w3

print(trigrams)

# Now we can do it one line:

trigrams = Grouping(((w1, w2), w3)
                    for w1, w2, w3 in zip(words[:], words[1:], words[2:]))
print(trigrams)

# Now with the key function:
# in thiscase it needs to be in a sequence, so we can't use a simple loop

trigrams = Grouping(zip(words[:], words[1:], words[2:]),
                    key_fun=itemgetter(0, 1))

print(trigrams)

# Darn! that got the key right, but the value is not right.
# we can post process:
trigrams = {key: [t[2] for t in value] for key, value in trigrams.items()}

print(trigrams)

# But THAT is a lot harder to wrap your head around than the original setdefault() loop!
# And it mixes key function style and comprehension style -- so no good.

# Adding a value_func helps a lot:
trigrams = Grouping(zip(words[:], words[1:], words[2:]),
                    key_fun=itemgetter(0, 1),
                    value_fun=itemgetter(2))

print(trigrams)

# That works fine, but I, at least, find it klunkier than the
# comprehensions style.

# Finally, we can use a regular loop with the functions

trigrams = Grouping(key_fun=itemgetter(0, 1),
                    value_fun=itemgetter(2))
for triple in zip(words[:], words[1:], words[2:]):
    trigrams.add(triple)

print(trigrams)




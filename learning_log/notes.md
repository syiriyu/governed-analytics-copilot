
# General Python

SEED is important because it retains the same randomisation for things we've specified it on. Makes our tests replicable.

Just like with DAX, we can use def to define reusable functions to keep our code cleaner.

Python uses indendation to understand what's included in your function. So when it comes to defining functions, you keep everything flush left if they're independent functions, and indent them if they're part of another function


# General NumPy

In the case of using rng functions, you have to specify your limit (low and high) & do + 1 because NumPy's upper limit excludes the absolute highest figure. So to get that true number, we need to add 1.


# General Pandas

Selecting one column is df["column"] ... selecting two columns is df[ ["column1", "column 2"] ]

For joins, setting validate=join_type validates the expected relationship when merging datasets - is useful for surfacing duplicated keys rather than silently showing dupe records
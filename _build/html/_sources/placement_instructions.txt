The placement_instructions.txt file
===========================================
The :file:`placement_instructions` file allows you to customize how placement will take place. It has two distinct sections. The sections are separated in the file by the presence of one or more empty lines.

.. module:: student

Placement Definitions
---------------------

The first section indicates the various possible placements, and it starts at the beginning of the file, until an empty line is encountered. Each placement can contain any number of keys. These can be used in templates (when creating letters for instance). The format for placements is as follows::

    placement_code1:
        key1: value1
        key2: value2
        etc
    placement_code2:
        key1: value1
        key2: value2
        etc

An unindented line ending in a colon indicates the code that the system will refer to address the placement. The indented :samp:`key: value` pairs represent characteristics of that placement. They can be used to customize input in templates. The indentation is important, make sure to preserve it! You should at the very least define keys :samp:`short` and :samp:`name`.

Placement Algorithm
-------------------
The second section dictates the algorithm for how to place a particular student, and it starts after the first empty line is encountered. Any number of empty lines might precede it. It comprises any number of lines of the form::

    expression => placement_code

Where :samp:`placement_code` is one of the codes defined in the first section, and :samp:`expression` is an expression that will be evaluated, and if it turns out to be :samp:`True` then the student will be placed in the corresponding placement and the search for a placement will end. The only tokens allowed in expressions are logicals, order operators, numerics, :samp:`None`, and the :samp:`is` operator. Any other token will be interpreted as either a key present in the student's dictionary, or if it is not a key it will be assumed to be an attribute of the student object. If it is callable it will be called. So for example the following line will place in Math 111 all students who have a placement score of 14 and above and have had pre-calculus, assuming that the Student object has an attribute :samp:`placement_score` and a function :samp:`has_precalc` returning :samp:`True` if the student has taken pre-calc, and false otherwise::

    placement_score >= 14 and has_precalc => Mat111

The expressions are evaluated in order till one is :samp:`True`. The last line of this section should *always* be::

     True => placement_code

This will indicate that if the student has not been placed with any of the previous test, this placement should be used.

Custom Functions
----------------

Currently there is no way to add custom instructions similar to :samp:`has_precalc`, but this is planned for the future. For a list of the currently available functions and attributes, see :class:`Student`.

Advanced
--------
The details of the processing of these expressions are performed in the :mod:`my_parser` module. In particular, the evaluation of word tokens is performed using the function :mod:`follow` and the methods that call it.

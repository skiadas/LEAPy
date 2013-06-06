import urllib
import re
import jinja2
import itertools
from my_parser import parse

def _splitrow(row):
	k, o = l.split(":")
	return((k.strip(), [x.strip() for x in [k] + o.split(",")]))

#: This dictionary contains for each field of the Student dictionary all the possible names that this field might be found under in a spreadsheet.
STUDENT_DICTIONARY = {}
with open("key_associations.txt", "r") as f:
    STUDENT_DICTIONARY = dict([_splitrow(l) for l in f])
#: Used for lookup. It reverses STUDENT_DICTIONARY
REVERSE_STUDENT_DICTIONARY = {}
for (key, val_list) in STUDENT_DICTIONARY.items():
    REVERSE_STUDENT_DICTIONARY.update([(val, key) for val in val_list])

def standardize_key(key):
    """Uses the key associations loaded from :file:`key_associations.txt` to standardize the value of `key`. Returns :samp:`None` if it does not find the key. This function is used by the :class:`student.Student` class to standardize the keys allowed by that class. The associations can be found in the file :file:`key_associations.txt`. Change the file at your own discretion."""
    k = key.lower()
    if STUDENT_DICTIONARY.has_key(k):
        return(k)
    elif REVERSE_STUDENT_DICTIONARY.has_key(k):
        return(REVERSE_STUDENT_DICTIONARY[k])
    else:
        return None
def standardize_keys(keys):
    """Standardizes a list of keys"""
    return [standardize_key(key) for key in keys]

class Placement:
    """The :class:`Placement` class forms an umbrella for all operations needed with regards to placement. It reads the information in :file:`placement_instructions.txt` to produce appropriate Singleton classes for each placement type, as well as the instructions on how to place a student. For more information on this file, see :doc:`placement_instructions`.
"""
    _placements = {}
    _expressions = []
    class __impl(dict):
        pass
        def __repr__(self):
            return(self.get('short', ""))
        def long(self):
            return(self.get('name', ""))
    # Populating _placements and __instructions
    @classmethod
    def _process_instructions(cls):
        """Used to process the information in :file:`placement_instructions.txt`. Not meant to be called."""
        with open("placement_instructions.txt") as f:
            all_lines = [l.rstrip() for l in f]
        newline = all_lines.index('')
        placements = all_lines[:newline]
        expressions = [l.split("=>") for l in all_lines[newline:] if not (l=='')]
        current = None
        for l in placements:
            if (l[0] in "\t "):
                current.append([x.strip() for x in l.split(":",1)])
            else:
                if (current is not None):
                    cls._placements[current[0]] = cls.__impl(dict(current[1:]))
                current = [l.split(":",1)[0].strip()]
        cls._placements[current[0]] = cls.__impl(dict(current[1:]))  # TODO: This is awkward, find better way to end the parsing.
        cls._expressions = [(l[0].strip(), cls._placements[l[1].strip()]) for l in expressions]

    @classmethod
    def Perform_placement(cls, student):
        """Goes through the list in :attr:`_expressions`, processing those expression for the current :samp:`student`, and returning the placement corresponding to the first True expression."""
        for expr, place in cls._expressions:
            if parse(expr, student):
                return(place)

Placement._process_instructions()
# Dictionary of helper functions, to be passed to the JINJA environments
helpers = {
    'room': lambda x: x.get('room', ''),
    'students_room': lambda rm, students: [st for st in students if st.get('room', '') == rm]
}

# Jinja2 environment to be used for exporting to LaTeX templates
JINJA_TEX_ENV = jinja2.Environment(
    block_start_string = '\pyblock{',
    block_end_string = '}',
    variable_start_string = '\pyvar{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%-',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader('templates')
)
JINJA_HTML_ENV = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'), trim_blocks = False)
for env in [JINJA_TEX_ENV, JINJA_HTML_ENV]:
    env.globals.update({'itools': itertools, 'helpers': helpers})
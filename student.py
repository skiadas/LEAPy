import re
from my_utils import standardize_key, Placement
# from string import Template
class Student(dict):
    """The Student class represents one student. It works as a dictionary but only accepts certain keys and automatically converts certain other keys to them. TODO create list of the keys. You usually don't need to work with this class directly, use :class:`studentList.StudentList` instead. Here are the main keys (this can be changed by editing the file :file:`key_associations.txt`):

    :var id: The student's id number.
    :var last: Last name
    :var first: First name
    :var nick: Nickname / Preferred name
    :var status: International student, Freshman etc
    :var act: ACT score (Math)
    :var sat: SAT score (Math)
    :var placement_score: The score in the placement exam
    :var placement_name: Deprecated. Use `placement` instead
    :var past_courses: A :samp:`&` separated list of abbreviations for courses the student took in High School. Used to determine for instance if the student has taken Calculus.
    :var placement: The student's placement. It is a :class:`my_utils.Placement` object.
    :var major: A :samp:`|` separated list of possible majors the student might be interested in.
    :var math_interest: y/n/m (maybe) depending on whether the student is interested in math.
    :var know_integrals: y/n depending on whether the student knows about integrals.
    :var room: The room the student is assigned for LEAP
    :var hc_grade: The student's average letter grade in High School
"""
    def __init__(self, *args, **kwargs):
            self.update(*args, **kwargs)
    def __getitem__(self, key):
        key = standardize_key(key)
        if key is None:
            return None
        return(dict.__getitem__(self, key))
    def get(self, key, default = None):
        """All getters and setters have been overwriten, in order for key standardization to take place."""
        key = standardize_key(key)
        if key in self:
            return self[key]
        else:
            return default
    def __setitem__(self, key, val):
        key = standardize_key(key)
        if key is not None:
            dict.__setitem__(self, key, val)
    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)
    def update(self, *args, **kwargs):
        """Replaces keys or adds new keys based on those provided, after standardizing them. This, along with :meth:`safe_update`, are the recommended method for updating :class:`Student` objects."""
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v
    def safe_update(self, *args, **kwargs):
        """Like :meth:`update` but will not change existing keys. Useful for merging information from new data sources."""
        for k, v in dict(*args, **kwargs).iteritems():
            if not self.has_key(k):
                self[k] = v
    def has_calc(self):
        """True if the student has taken Calculus."""
        if self.get('past_courses',''):
            past = self['past_courses'].split("&")
            return(('calc' in past) or ('APCalc' in past))
        return(False)
    def has_precalc(self):
        """True if the student has taken pre-Calculus."""
        if self.get('past_courses',''):
            return('precalc' in self['past_courses'].split("&"))
        return(False)
    def is_premed(self):
        """True if the student is interested in pre-med."""
        if self.get('major',''):
            return('pre-med' in self['major'].split("|"))
        return(False)
    def calc_credit(self):
        """True if the student is likely to have Calculus AP or college credit."""
        if self.get('survey_result','') == '2':
            return(True)
        return(False)
    def needs_calc(self):
        """True if the student is in a major that requires Calculus."""
        return(not(self.get('major','') == "" or self.get('major','') is None))
    def wants_calc(self):
        """True if the student has indicated they would like to take Calculus even if not required."""
        return(self.get('interest', '') == 'y')
    def needs_wants_calc(self):
        return(self.needs_calc() or self.wants_calc())
    def has_placement(self):
        return(self["placement"] is not None)
    def took_test(self):
        if self.get('placement_score','') is not None:
            return(True)
        return(False)
    # def premed_line(self):
    #   if self.is_premed():
    #       return("You should talk with your pre-med advisor about whether or not to take calculus your first semester (Fall \\the\\year).")
    #   else:
    #       return("")

    def perform_placement(self):
        """Uses :meth:`my_utils.Placement.Perform_placement` to assign a placement to the student."""
        self['placement'] = Placement.Perform_placement(self)


from my_utils import JINJA_TEX_ENV, JINJA_HTML_ENV
from student import Student, standardize_key
from dataset_utils import Dataset
class StudentList(list):
    """Initialize a :class:`StudentList` object using provided data. The provided object needs to act as a list of dictionaries. Those dictionaries are passed to the :class:`student.Student` class to form the individual student objects. A typical way to obtain such a list is via a `dataset_utils.Dataset` object.
    
    Use :meth:`update_from_dataset` to add new key entries to the students, meth:`perform_placement` to place them according to the rules set (see :class:`my_utils.Placement`), meth:`dataset` to convert to a spreadsheet/dataset format, :meth:`export_to_template` for generating reports."""
    def __init__(self, lst):
        super(StudentList, self).__init__()
        for dct in lst:
            self.append(Student(dct))

    def update_from_dataset(self, key, sheet, force_update = False, target_key=None):
        """Updates any students common to :samp:`self` and :samp:`sheet` with the information in them. Will use the values described by :samp:`key` and :samp:`target_key` respectively to identify which students in the two datasets match. :samp:`sheet` needs to be :class:`dataset_utils.Dataset` object. If :samp:`force_changes` is :samp:`True`, the method will update the values of any keys that are present in :samp:`sheet`, overwriting any possibly existing values. This will rarely be what you want. If :samp:`target_key` is :samp:`None`, it will use the same key on both datasets. The conversions in :meth:`my_utils.standardize_key` are in place."""
        if target_key is None:
            key = standardize_key(key)
            target_key = key
        else:
            key = standardize_key(key)
        for st in self:
            for row in sheet:
                if st[key] == row[target_key]:
                    if force_update:
                        st.update(row)
                    else:
                        st.safe_update(row)
                    break
    def perform_placement(self):
        """Simple wrapper for :meth:`student.Student.perform_placement`. Attempts to assign a placement to every student."""
        for val in self:
            val.perform_placement()

    def dataset(self, keys = []):
        """Returns :samp:`self` in a dataset format. Uses all keys present unless a list is specified."""
        if keys == []:
            keys = set()
            for i in self:
                keys.update(i.keys())
        return(Dataset([keys] + [[st.get(key) for key in keys] for st in self]))

    def export_template(self, template, format=None, sortby = None):
        """Exports the student information according to the template specified. LaTeX or HTML output is possible by setting :samp:`format='tex'` or :samp:`'html'`. If no format specified, and the template is a filename string, it will use the extension to determine the format. Returns the output stream. See :doc:`template_creation` for more information on templates."""
        if isinstance(template, str) and format is None:
            format = template.rsplit(".",1)[1]
        env = { 'tex': JINJA_TEX_ENV, 'html': JINJA_HTML_ENV}[format]
        students = self
        if sortby is not None:
            students = sorted(students, key = sortby)
        return(env.get_template(template).render({'students': students}))

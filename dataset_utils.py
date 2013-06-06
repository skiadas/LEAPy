import re
import xlrd
import xlwt
import itertools
import csv
import urllib
from itertools import izip, count, cycle, repeat
from my_utils import JINJA_TEX_ENV, JINJA_HTML_ENV, standardize_keys

def fix_col(lst):
    """A helper function attempting to uniformize the items in a list (data column). If a column consists of only strings representing numbers, turns them to numbers. Treats empty strings as missing values and replaces them with None."""
    def _try_convert(val):
        if val=='':
            return(None)
        else:
            try:
                return(int(val))
            except:
                try:
                    return(float(val))
                except:
                    return val
    return([_try_convert(val) for val in lst])

class Dataset:
    """The :class:`Dataset` class models a basic dataset/spreadsheet functionality. It can read and write Excel sheets, CSV and HTML tables. It implements a basic iteration over its rows, where each row is returned as a dictionary, with the variable/column names as keys."""
    _FILE_ASSOCIATIONS = {'csv': ['csv', 'txt'], 'excel': ['xls'], 'html': ['html', 'htm']}
    def __init__(self, data):
        """Expects a list of rows. First entry is variable names. """
        self.varnames = list(data[0])
        self.rows = [list(val) for val in data[1:]]
        self.cols = [fix_col(list(val)) for val in zip(*self.rows)] # Turns numeric values to such
        self.rows = [list(val) for val in zip(*self.cols)]
        self.dict = [dict(zip(self.varnames, row)) for row in self.rows]
    def __iter__(self):
        return(self.dict.__iter__())
    # def next(self):
    #   self.dict.next()
    def get_col(self, col):
        """Returns the columns described by :samp:`col`. Accepts column descriptions as either a number starting at 0 or column name, or as a list of the same."""
        if (isinstance(col, list)):
            return([self.get_col(val) for val in col])
        elif (isinstance(col, str)):
            return(self.get_col(self.varnames.index(col)))
        else: # It's an integer
            return(self.cols[col])
    def get_row(self, row):
        """Returns the rows described by :samp:`row`. Accepts row descriptions as either a number or a list of numbers."""
        if (isinstance(row, list)):
            return([self.get_row(val) for val in list])
        else:
            return(self.rows[row])
    
    @classmethod
    def _Read_csv(cls, dataset):
        """"""
        rdr = csv.reader(dataset)
        return(Dataset([x for x in rdr]))
        
    @classmethod
    def _Read_excel(cls, dataset):
        """Note: Will only attempt to read the first sheet from the Excel file"""
        sheet = xlrd.open_workbook(file_contents=dataset.read()).sheet_by_index(0)
        ncols, nrows = sheet.ncols, sheet.nrows
        rows = [sheet.row_values(i) for i in range(nrows)]
        # validrows = [row for row in rows if (row)[ncols-1] is not '']
        # print(validrows)
        return(Dataset(rows))
        
    @classmethod
    def _Read_html(self, dataset):
        """docstring for read_html"""
        if not isinstance(dataset, str):
            dataset = dataset.read()
        table_regex = re.compile("<table .*?>(.*?)</table>", re.DOTALL)
        row_regex = re.compile("<tr.*?>(.*?)</tr>", re.DOTALL)
        entry_regex = re.compile("<t[dh].*?>(.*?)</t[dh]>", re.DOTALL)
        m = table_regex.match(dataset)
        if m is not None:
            dataset = m.group(1)
        return(Dataset([entry_regex.findall(row) for row in row_regex.findall(dataset)]))
    @classmethod
    def Read(cls, dataset, filetype = None, raw=False):
        """Reads datasets in either an Excel or a CSV form, or from a HTML table. Expects first row to be variable names, every subsequent row to be data, and that no extra rows are present. Returns the result as a :class:`Dataset` object. Only understands character and numeric data at this point."""
        # Check if dataset looks like a filename: It would basically be all in one line and have
        # an extension
        if isinstance(dataset, str) and not raw:
            m = re.match("^(.*)\.([^\.]*)$", dataset)
            if (m is not None):   # filename!!
                if filetype is None:
                    filetype = m.group(2)   # Pick up filetype from extension if not provided
                    for (k,v) in cls._FILE_ASSOCIATIONS.items():
                        if filetype in v:
                            filetype = k
                readformat =  'rb' if (filetype == 'excel') else 'r'
                with open(dataset, readformat) as _data:
                    return(cls.Read(_data, filetype))
        else:
            # dataset contains our actual data stream
            call = {'csv': cls._Read_csv, 'excel': cls._Read_excel, 'html': cls._Read_html}.get(filetype)
            if call is None:
                raise(TypeException, "Unknown file type: %s" % filetype)
            else:
                return(call(dataset))
    @classmethod
    def Read_survey(cls):
        """Helper method, that reads the data from the math survey that students have to take."""
        results = urllib.urlopen("http://exam.hanover.edu/tests/math1/list_results.php").read()
        if re.search("Math Placement Survey Results", results) is None:
            raise IOError("Encountered problems trying to read the Interest Survey Results. Please make sure the web site is available: http://exam.hanover.edu/tests/math1/list_results.php")
        tbl = re.compile("<table>(.*?)</table>", re.DOTALL).search(results).group(1)
        tbl = re.sub("</?a[^>]*>", "", tbl) # Stripping <a> tags
        return(cls.Read(tbl, 'html', raw = True))

# Exporting Facilities
    def _export_html(self, file, keys = [], key_names = [], *args, **kwrds):
        """Use :meth:`export` instead.
        
        The keywords following will decorate the html tags. Each expects a list of dictionaries, and will alternate those dictionaries on consecutive cells:

        :var row_decorations: Used on the <tr> tag of the data rows
        :var row_cell_decorations: Used on the <td> tags of the data rows
        :var var_decoration: Only one dictionary, used on the <tr> tag of the variables row
        :var var_cell_decorations: Used on the <td> tags of the variables row
        """
        dictionary = dict(*args, **kwrds)
        dictionary.update({ 'keys':  keys, 'rows': self.dict, 'key_names': key_names})
        for key in ['var_cell_decorations', 'row_cell_decorations', 'row_decorations']:
            dictionary[key] = cycle(dictionary.get(key, [{}]))
        dictionary["var_decoration"] = dictionary.get("var_decoration", {})
        env = JINJA_HTML_ENV
        # This part feels ugly
        env.globals.update({'dictionary': dictionary})
        template = env.get_template('html_table_template.html')
        file.write(template.render(dictionary))
    
    def _export_excel(self, file, sheet_name = "Sheet 1", keys = [], key_names = [], *args, **kwds):
        """Don't call directly. Use :meth:`export` instead."""
        heading_xf = xlwt.easyxf('font: bold on; align: wrap off, vert centre, horiz center; border: left thin, right thin, bottom thin, top thin')
        row_xf = xlwt.easyxf('border: left thin, right thin')
        wbook = xlwt.Workbook()
        sheet = wbook.add_sheet(sheet_name)
        for j, key, key_name in izip(count(0), keys, key_names):
            sheet.write(0, j, key_name, heading_xf)
            for i, st in izip(count(1), self.dict):
                val = st.get(key,"")
                val = "" if val is None else str(val)
                sheet.write(i,j, val , row_xf)
        wbook.save(file)


    def export(self, file, keys=[], key_names = [], format = None, *args, **kwds):
        """Exports the dataset to an appropriate format, automatically detected by :samp:`file` if it is an actual filename. If no :samp:`keys` are provided, it will use all of them, this is not typically what you want. You may provide :samp:`key_names` to have those appear at the column headers instead."""
        if key_names and not keys:
            raise KeyException, "keys need to be provided if key_names are provided."
        keys = keys or self.varnames
        key_names = key_names or keys
        keys = standardize_keys(keys)
        format = format or file.rsplit(".")[-1]
        func = {
            "html": self._export_html,
            "xls": self._export_excel,
            "excel": self._export_excel
        }[format]
        writeformat =  'wb' if (format == 'excel' or format == 'xls') else 'w'
        with (file if hasattr(file, "write") else open(file, writeformat)) as f:
            return(func(file = f, keys = keys, key_names = key_names, *args, **kwds))

    def subset(self, row_tester):
        """:samp:`row_tester` is a function that takes a dictionary representing a row, and returns whether that row should be included in the subset."""
        new_dict = [row for row in self.dict if row_tester(row)]
        final_list = [self.varnames] + [[row[var] for var in self.varnames] for row in new_dict]
        return(Dataset(final_list))
# with open("tests/Leap5_math_placements.xls", "rb") as dataset:
#   sheet = xlrd.open_workbook(file_contents=dataset.read()).sheet_by_index(0)
#   ncols, nrows = sheet.ncols, sheet.nrows
#   rows = [sheet.row_values(i) for i in range(nrows)]
#   validrows = [row for row in rows if (row)[ncols-1] is not '']
#   return(Dataset(validrows))

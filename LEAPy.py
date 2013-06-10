from dataset_utils import Dataset
from studentList import StudentList
import itertools as itools
import my_utils
from string import Template
import os
import os.path

cwd = os.getcwd()
# Set these options
LEAP_FOLDER = "2013LEAP3"
LETTER_TEMPLATE = "tex_letter_template_barb.tex"
ROOMS_TEMPLATE = "tex_rooms_template.tex"

if not(os.path.isdir(LEAP_FOLDER)):
    raise Exception("LEAP Folder does not exist:", LEAP_FOLDER)

os.chdir(LEAP_FOLDER)

# These file should exist
PLACEMENT_FILE = "PlacementTests.csv"
EXCEL_FILE = "MathLEAP.xls"
ROOMS_EXCEL_FILE = "LEAPRooms.xls"

# The following files will be created
OUPUT_EXCEL = "Output.xls"
OUTPUT_JAN = "OutputJan.xls"
OUTPUT_HTML = "Output.html"
OUTPUT_LETTERS_TEX = "OutputLetters.tex"
OUTPUT_ROOMS_TEX = "OutputRooms.tex"

# Reading the data in
interest_survey = Dataset.Read_survey()
scores = Dataset.Read(PLACEMENT_FILE) # from Maplesoft site -- download scores in CSV
students = StudentList(Dataset.Read(EXCEL_FILE)) # first excel file from Jan
students.update_from_dataset("id", scores, target_key = "Student ID")
students.update_from_dataset("id", interest_survey, target_key = "ID")
students.perform_placement()
studexp = students.dataset()

studexp.export(keys = ["id_num", "last_name", "first_name", "preferred", "actmt", "satm", "major", "courses", "placement score", "survey_result", "placement"],
    file = OUPUT_EXCEL)
# studexp.export(keys = ["id_num", "last_name", "first_name", "preferred", "actmt", "satm", "major", "courses", "placement score", "survey_result", "placement"], 
#     file = OUTPUT_HTML, var_decoration = {'bgcolor':'#dd0000'}, row_decorations = [{'bgcolor':'#dddddd'}, {'bgcolor':'#cccccc'}])

# This is the key command, preparing the documents for Jan
studexp.export(keys = ["id_num", "last_name", "first_name", "preferred", "placement score", "placement"], 
    file = OUTPUT_JAN)

test_placement = lambda st: not(st.get("placement").get("code") == 'none')
students = StudentList(students.dataset().subset(test_placement))

with open(OUTPUT_LETTERS_TEX, "w") as f:
  os.chdir(cwd)
  f.write(students.export_template(LETTER_TEMPLATE, sortby = lambda st: st['last_name']))

os.chdir(LEAP_FOLDER)
# Reading students for Room printouts
students2 = StudentList(Dataset.Read(ROOMS_EXCEL_FILE))
students2.update_from_dataset("id", scores, target_key = "Student ID")
students2.update_from_dataset("id", interest_survey, target_key = "ID")
students2.perform_placement()


with open(OUTPUT_ROOMS_TEX, "w") as f:
  os.chdir(cwd)
  f.write(students2.export_template(ROOMS_TEMPLATE, sortby = lambda st: st['room']))
# 

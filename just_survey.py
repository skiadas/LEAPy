from dataset_utils import Dataset
from studentList import StudentList
import itertools as itools
import my_utils

# Reading the data in
interest_survey = Dataset.Read_survey()
print interest_survey
# interest_survey.export(keys = ["id", "last_name", "first_name", "preferred", "actmt", "satm", "major", "courses", "placement score", "placement"], file="survey_results.xls")



# scores = Dataset.Read("LEAPFiles/LEAP6PlacementTests.csv") # from Maplesoft site -- download scores in CSV
# students = StudentList(Dataset.Read("LEAPFiles/math_leap6.xls")) # first excel file from Jan
# students.update_from_dataset("id", scores, target_key = "Student ID")
# students.update_from_dataset("id", interest_survey, target_key = "ID")
# students.perform_placement()
# studexp = students.dataset()
# 
# 
# studexp.export(keys = ["id_num", "last_name", "first_name", "preferred", "actmt", "satm", "major", "courses", "placement score", "placement"], file = "testingoutput.xls")
# studexp.export(keys = ["id_num", "last_name", "first_name", "preferred", "actmt", "satm", "major", "courses", "placement score", "placement"], file = "testingoutput.html", var_decoration = {'bgcolor':'#dd0000'}, row_decorations = [{'bgcolor':'#dddddd'}, {'bgcolor':'#cccccc'}])
# 
# # This is the key command, preparing the documents for Jan
# studexp.export(keys = ["id_num", "last_name", "first_name", "preferred", "placement score", "placement"], file = "PlacementsForJan6.xls")
# 
# # Reading students for Room printouts
# students2 = StudentList(Dataset.Read("LEAPFiles/LEAP6Rooms.xls"))
# students2.update_from_dataset("id", scores, target_key = "Student ID")
# students2.update_from_dataset("id", interest_survey, target_key = "ID")
# students2.perform_placement()
# 
# test_placement = lambda st: not(st.get("placement").get("code") == 'none')
# students2 = StudentList(students2.dataset().subset(test_placement))
# 
# with open("testing.tex", "w") as f:
#   f.write(students2.export_template('tex_letter_template.tex', sortby = lambda st: st['room']))
# 

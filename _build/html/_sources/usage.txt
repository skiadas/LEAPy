************
Using LEAPy
************

This contains high-end information on how to use LEAPy. For more in-depth information on each of these options, see :doc:`developer`.

In brief, LEAPy offers us tools to read and process spreadsheets containing student information, as well as produce reports based on this information.

Typical code segment
====================

We first need to load the basic classes used, :class:`Dataset` and :class:`StudentList`::

    from dataset_utils import Dataset
    from studentList import StudentList

Next, we should load a student list from a dataset. In this case we will use an old Leap placement file::

    students = StudentList(Dataset.Read("LEAPFiles/Leap5_math_pre_placement.xls"))

We will now merge this with information obtained from another dataset::

    students.update_from_dataset("Last", Dataset.Read("tests/placement_test_scores.csv"), target_key = "Last")

The string :samp:`"Last"` and the accompanying :samp:`target_key = "Last"` indicate that the Last name of the students in our list should be matched with the column with name Last from the dataset we read in. The program will identify the students that get matched this way, and it will update their information in the list from the new fields found in the dataset. It will NOT attempt to change existing keys.

We have now a list of students who have received placement score information from this last command. The next step is to actually perform the placement process::

    students.perform_placement()

Now that our students have placement information, we can generate their letters::

    with open("testing.tex", "w") as f:
        f.write(students.export_template('tex_letter_template.tex')

Ideally we would include room information.

That's all for now! Look in :doc:`developer` for basic descriptions of the classes and their main methods, as well as all the finer details of the package.

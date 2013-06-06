General Overview
================
The functionality of LEAPy revolves around the following classes. Only a brief preview provided here, look at their individual pages for more details.

* :class:`student.Student`   Corresponds to the record of a single student. 
* :class:`studentList.StudentList`    A list of students read form a spreadsheet/dataset. This is the main object we work with.
* :class:`dataset_utils.Dataset`   Helper class that allows reading and writing datasets in various formats, CSV, Excel and HTML currently supported.

.. currentmodule:: studentList

Typically we use :meth:`dataset_utils.Dataset.Read` to process a dataset from a file/string, then use :class:`StudentList`'s constructor to create a :class:`StudentList` object. Merge information from another dataset using :meth:`StudentList.update_from_dataset`. To produce an output based on the student list, use :meth:`StudentList.export_template`.

Some important files:

* :file:`key_associations.txt` This file contains the associations between internal keys for the :class:`Student` class and other names for those keys, which may be encountered when reading a dataset. The entries are case insensitive. Any key provided that is not specified in that file will be silently ignored. You may edit this file to add new keys or associations. The format is always: :samp:`key: association1, association2, etc`.
* :file:`placement_instructions.txt` This file dictates how placement is to be made. See :doc:`placement_instructions` for a detailed description.

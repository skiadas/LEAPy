1. Create a new folder named after the year and the leap, e.g. '2013LEAP3'.
2. Get Excel file from Jan, save it in this new folder as `mathLEAP.xls`. Use Excel to save it in the older Excel format (97/2003?).
3. Log in to MapleTA, click the 'math placement test' class. Choose 'Gradebook -> Search -> Class Grades'
4. Under Assignments find 'Hanover College Calculus Placement Exam' after all the Algorithmic courses. Select it.
5. Under 'User Data' select 'Student ID'.
6. Under 'Summary Data' deselect 'Total points'.
7. Click on 'Search', then 'Export CSV'.
8. Save the resulting file in the new folder as `PlacementTests.csv`.
9. When we get the rooms file from Jan, save in the new folder in old Excel format as 'LEAPRooms.xls'.
10. In `templates/tex_letter_template_barb.tex` make any desired changes to the end of the letter.
11. In the file `LEAPy.py`, adjust the `LEAP_FOLDER` variable in line 11, save and run it through Python.
12. If you get no errors, use LaTeX to compile the files `OutputLetters.tex` and `OutputRooms.tex` in the new folder.
13. You are done!

The output files are as follows, all in the folder you created:

- `Output.xls`: An Excel file with detailed placement information on everyone
- `OutputJan.xls`: The Excel file with the placements to send to Jan
- `OutputLetters.pdf`: The pdf file with the letters, to be printed on fancy paper and given to Angie
- `OutputRooms.pdf`: A small pdf file listing the students and their placement/interests by room. Print and bring with you.

Also useful is a file named `MathGuideForAdvisors.pdf` in the root folder. Print and give copies to the various advisors.
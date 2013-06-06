Creating Templates
==================

Templates use the `Jinja2 <http://jinja.pocoo.org/docs/>`_ templating system. They have access to the :meth:`studentList.StudentList` dictionary that is part of their call. Here's a typical example of calling a template::

    with open("testing.tex", "w") as f:
        f.write(students.export_template('tex_letter_template.tex', sortby = lambda st: st['room']))

Here :samp:`students` is a :meth:`studentList.StudentList` object, whose attributes are available to the template. You can pass a function to :samp:`sortby` if you want the student list to be traversed in a particular order. The template can be in LaTeX or HTML, and it basically consists of standard language code, except for special directives containing python code, that are executed by the parser. Here is the example from :file:`templates/tex_letter_template.tex`, with nonessential parts removed:

.. code-block:: latex
   :linenos:
   
   \documentclass[12pt]{article}
   \usepackage[vmargin=1in, hmargin=1in]{geometry}
   \begin{document}

   \pyblock{for rm, stds in itools.groupby(students, helpers.room)}
    \newpage
    \begin{center}
    \textbf{Room\\
    \pyvar{rm}}
    \vfill
    \pyblock{for st in helpers.students_room(rm, students)}
        \pyvar{st.last}, \pyvar{st.first}\\
    \pyblock{endfor}
    \end{center}
    \vfill
    \pyblock{for st in stds}
        \newpage
        {\Large Student: \pyvar{st.last}, \pyvar{st.first}\\
        Placement: \pyvar{st.placement.short} (\pyvar{st.placement.name})
        }
        \noindent\today\\
        \noindent Dear \pyvar{st.first},

        Thank you for taking the calculus interest survey ...  the Math department recommends you begin calculus at Hanover by taking \pyvar{st.placement.short}.  
        \pyblock{if st.is_premed()}
            You should talk with your pre-med advisor about whether or not to take calculus your first semester (Fall \the\year).
        \pyblock{endif}

        \noindent Best regards,\\
        Barbara Wahl\\
        Department of Mathematics \& Computer Science\\
        Hanover College\\
    \pyblock{endfor}
   \pyblock{endfor}
   \end{document}

In LaTeX documents there are two kinds of special directives: :samp:`\pyblock` and :samp:`\pyvar`. The former is used for  control structures, the latter for evaluating expressions. For instance, the :samp:`\pyblock` in line 5 starts an iteration over all pairs of students and corresponding room. This block ends with the :samp:`\pyblock` on line 34. The text inbetween is repeated once for every pair of a room and all the students assigned to that room. In line 9, :samp:`\pyvar{rm}` gets replaced by the actual value of :samp:`rm`, which is the room number. Lines 11-13 create a list of all the first and last names of all the students in that room. And so on.

HTML templates are very similar. Here is an example from :file:`templates/html_table_template.html`, which is used by the :meth:`dataset_utils.Dataset.export_html` method:

.. code-block:: html
   :linenos:

   <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
   <html>
   <body>
    <table>
        <tr {{- var_decoration|xmlattr }}>
        {%- for (dec, key) in itools.izip(var_cell_decorations, key_names) -%}
            <th {{- dec|xmlattr }}>{{ key }}</th>
        {%- endfor -%}
        </tr>
        {%- for (dec, st) in itools.izip(row_decorations, rows) %}
        <tr {{- dec|xmlattr }}>
        {%- for (dc, key) in itools.izip(row_cell_decorations, keys) -%}
            <td {{- dc|xmlattr }}>{{ st[key] or '' }}</td>
        {%- endfor -%}
        </tr>
        {%- endfor %}
    </table>
   </body>
   </html>

Here the blocks starting with :samp:`{{` are the analogs of :samp:`\pyvar`, while the blocks starting with :samp:`{%` are the analogs of :samp:`\pyblock`. Consult the Jinja2 documentation for more details on these.

   
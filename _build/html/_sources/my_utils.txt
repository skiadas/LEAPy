The :mod:`my_utils` Module
==========================

The :mod:`mu_utils` module contains certain constants and helper functions, in addition to the :class:`Placement` class, which performs the actual grunt work of placing students based on a given set of rules.

.. automodule:: my_utils
   :members: standardize_key

.. data:: JINJA_TEX_ENV

    The Jinja2 environment used for LaTeX templates. See :doc:`template_creation` for more details.

.. data:: JINJA_HTML_ENV

    The Jinja2 environment used for HTML templates. See :doc:`template_creation` for more details.

The :class:`Placement` class
----------------------------

   .. autoclass:: Placement
      :members:
      
      .. attribute:: _placements

      A dictionary of possible placements. The values are objects of a private class, whose attributes and corresponding values are the pairs specified for that placement in :file:`placement_instructions.txt` and are read at start-up.

      .. attribute:: _expressions

      A list of pairs :samp:`(expression, placement)`, where :samp:`expression` is an expression to be evaluated for each student, the :samp:`placement` is the corresponding placement key, from :attr:`_placements`.

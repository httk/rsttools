========
rstslide
========

-------------
Demonstration
-------------

.. These include lines add some features
   which are explained on the slides titled 'includes'

.. include:: <s5defs.txt>
.. include:: <isonum.txt>

.. Below follows the docinfo segment

   There are four types of docinfo fields, each grouped by double newline below.

   1. Those with defined bibliographic meaning in rst.

   2. The abstract and dedication are defined in rst to be lifted out of the docinfo,
      and are meant to be typeset somehow in the document.

   3. Non-rst fields that have defined meaning in rstslide.
      This is how you set configuration options.

   4. Non-rst fields with no meaning in rstslide.
      These are ignored.

   Note: one cannot put comments inside the docinfo block.
   Only the first field list counts as part of the docinfo, and
   a comment ends it.

:author: Rickard Armiento
:authors:
    Example Author 1
    Example Author 2
    Example Author 3
:address: 123 Example Street
	  Example, EX  Canada
	  A1B 2C3
:contact: Telephone: 555-1234
          Fax: 555-4711
          Email: example@example.com
:copyright: This document has been placed in the public domain.
	    You may do with it as you wish. You may copy, modify,
	    redistribute, reattribute, sell, buy, rent, lease, destroy,
	    or improve it, quote it at length, excerpt, incorporate,
	    collate, fold, staple, or mutilate it, or do anything else to
	    it that your or anyone else's heart desires.
:date: August 2020
:organization: humankind
:status: This is a "work in progress"
:version: 1
:revision: 8524

:abstract: This document attempts
           to be a fairly complete
           guide to everything that
           can be done in rstslide

:dedication: To my better judgement.


:email:
:theme: default
:note: (rstslide was forked from rst2reveal by Julien Vitay
       and this document is based on the 'reStructuredText Demonstration' document)

:test: These fields can span
       over multiple lines
       without a problem.
:parameter i: integer
:test-nolist: this, contains, many, things
:test-list: this, contains, many, things
:test2-list: - this
             - contains
             - many
             - things

:css_embedd-list-add:
      #toc-progress-footer-main
      {
      background-image: url("logo.svg");
      }

.. The final entry above adds a logo to the footer bar.

.. meta::
   :keywords: reStructuredText, demonstration, demo, parser
   :description lang=en: A demonstration of the reStructuredText
       markup language, containing examples of all basic
       constructs and many advanced constructs.

.. It is nice with a table of contents for the handouts, but
   not for slides.

.. class:: handout

.. contents:: Table of Contents


Structural Elements
===================

Section Title
-------------

That's it, the text just above this line.

::

  Section Title
  -------------

  That's it, the text just above this line.

Transitions
-----------

Here's a transition:

---------

It divides the section.

::

  Here's a transition:

  ---------

  It divides the section.

Body Elements
=============

Inline markup
-------------

Paragraphs contain text and may contain inline markup: *emphasis*,
**strong emphasis**, ``inline literals``, standalone hyperlinks
(http://www.python.org), external hyperlinks (Python_), internal
cross-references (example_), external hyperlinks with embedded URIs
s(`Python web site <http://www.python.org>`__), footnote references
(manually numbered [1]_, anonymous auto-numbered [#]_, labeled
auto-numbered [#label]_, or symbolic [*]_), citation references
([CIT2002]_), substitution references (|example|), and _`inline
hyperlink targets` (see Targets_ below for a reference back to here).

Character-level inline markup is also possible in *re*\ ``Structured``\ *Text*.

.. |EXAMPLE| image:: logo-black.svg
		     :width: 5em
		     :align: middle

::

  Paragraphs contain text and may contain inline markup: *emphasis*,
  **strong emphasis**, ``inline literals``, standalone hyperlinks
  (http://www.python.org), external hyperlinks (Python_), internal
  cross-references (example_), external hyperlinks with embedded URIs
  (`Python web site <http://www.python.org>`__), footnote references
  (manually numbered [1]_, anonymous auto-numbered [#]_, labeled
  auto-numbered [#label]_, or symbolic [*]_), citation references
  ([CIT2002]_), substitution references (|example|), and _`inline
  hyperlink targets` (see Targets_ below for a reference back to here).

  Character-level inline markup is also possible in *re*\ ``Structured``\ *Text*.

  .. |EXAMPLE| image:: logo-black.svg
  		       :width: 5em
		       :align: middle


Footnotes
---------

.. class:: tiny

  .. [1] A footnote contains body elements, consistently indented by at
     least 3 spaces.

     This is the footnote's second paragraph.

  .. [#label] Footnotes may be numbered, either manually (as in [1]_) or
     automatically using a "#"-prefixed label.  This footnote has a
     label so it can be referred to from multiple places, both as a
     footnote reference ([#label]_) and as a hyperlink reference
     (label_).

  .. [#] This footnote is numbered automatically and anonymously using a
     label of "#" only.

  .. [*] Footnotes may also use symbols, specified with a "*" label.
     Here's a reference to the next footnote: [*]_.

  .. [*] This footnote shows the next symbol in the sequence.

  .. [4] Here's an unreferenced footnote.

  .. [CIT2002] Citations are text-labeled footnotes. They may be
     rendered separately and differently from footnotes.

  Here's a reference to the above, [CIT2002].

.. class:: tiny

::

  .. [1] A footnote contains body elements, consistently indented by at
     least 3 spaces.

     This is the footnote's second paragraph.

  .. [#label] Footnotes may be numbered, either manually (as in [1]_) or
     automatically using a "#"-prefixed label.  This footnote has a
     label so it can be referred to from multiple places, both as a
     footnote reference ([#label]_) and as a hyperlink reference
     (label_).

  .. [#] This footnote is numbered automatically and anonymously using a
     label of "#" only.

  .. [*] Footnotes may also use symbols, specified with a "*" label.
     Here's a reference to the next footnote: [*]_.

  .. [*] This footnote shows the next symbol in the sequence.

  .. [4] Here's an unreferenced footnote, with a reference to a
     nonexistent footnote: [5]_.

  .. [CIT2002] Citations are text-labeled footnotes. They may be
     rendered separately and differently from footnotes.

  Here's a reference to the above, [CIT2002].


Targets
-------

.. _example:

This paragraph is pointed to by the explicit "example" target. A
reference can be found under `Inline Markup`_, above. `Inline
hyperlink targets`_ are also possible.

Section headers are implicit targets, referred to by name. See
Targets_, which is a subsection of `Body Elements`_.

Explicit external targets are interpolated into references such as
"Python_".

.. _Python: http://www.python.org/

Targets may be indirect and anonymous.  Thus `this phrase`__ may also
refer to the Targets_ section.

__ Targets_



Text roles
----------
Here are some explicit interpreted text roles: a PEP reference (:PEP:`287`); an
RFC reference (:RFC:`2822`); a :sub:`subscript`; a :sup:`superscript`;
and explicit roles for :emphasis:`standard` :strong:`inline`
:literal:`markup`.

Let's test wrapping and whitespace significance in inline literals:
``This is an example of --inline-literal --text, --including some--
strangely--hyphenated-words.  Adjust-the-width-of-your-browser-window
to see how the text is wrapped.  -- ---- --------  Now note    the
spacing    between the    words of    this sentence    (words
should    be grouped    in pairs).``

::

  Here are some explicit interpreted text roles: a PEP reference (:PEP:`287`); an
  RFC reference (:RFC:`2822`); a :sub:`subscript`; a :sup:`superscript`;
  and explicit roles for :emphasis:`standard` :strong:`inline`
  :literal:`markup`.

  Let's test wrapping and whitespace significance in inline literals:
  ``This is an example of --inline-literal --text, --including some--
  strangely--hyphenated-words.  Adjust-the-width-of-your-browser-window
  to see how the text is wrapped.  -- ---- --------  Now note    the
  spacing    between the    words of    this sentence    (words
  should    be grouped).``


Bullet Lists
------------

.. container::
     :class: column-50

  - A bullet list

    + Nested bullet list.
    + Nested item 2.

  - Item 2.

    Paragraph 2 of item 2.

    * Nested bullet list.
    * Nested item 2.

      - Third level.
      - Item 2.

    * Nested item 3.

.. container::
     :class: column-50

  ::

    - A bullet list

      + Nested bullet list.
      + Nested item 2.

    - Item 2.

      Paragraph 2 of item 2.

      * Nested bullet list.
      * Nested item 2.

	- Third level.
	- Item 2.

      * Nested item 3.

      
Enumerated Lists
----------------

.. container::
     :class: column-50

  1. Arabic numerals.

     a) lower alpha)

	(i) (lower roman)

	    A. upper alpha.

	       I) upper roman)

  2. Lists that don't start at 1:

     3. Three

     4. Four

     C. C

     D. D

     iii. iii

     iv. iv

  #. List items may also be auto-enumerated.

.. container::
     :class: column-50

  ::

    1. Arabic numerals.

       a) lower alpha)

	  (i) (lower roman)

	      A. upper alpha.

		 I) upper roman)

    2. Lists that don't start at 1:

       3. Three

       4. Four

       C. C

       D. D

       iii. iii

       iv. iv

    #. List items may also be auto-enumerated.


Definition Lists
----------------

.. container::
     :class: column-50

  Term
      Definition
  Term : classifier
      Definition paragraph 1.

      Definition paragraph 2.
  Term
      Definition

.. container::
     :class: column-50

  ::

    Term
	Definition
    Term : classifier
	Definition paragraph 1.

	Definition paragraph 2.
    Term
	Definition

Field Lists
-----------

:what: Field lists map field names to field bodies, like database
       records.  They are often part of an extension syntax.  They are
       an unambiguous variant of RFC 2822 fields.

:how arg1 arg2:

    The field marker is a colon, the field name, and a colon.

    The field body may contain one or more body elements, indented
    relative to the field marker.

Option Lists
------------

.. class:: tiny

  For listing command-line options:

  -a            command-line option "a"
  -b file       options can have arguments
		and long descriptions
  --long        options can be long also
  --input=file  long options can also have
		arguments

  --very-long-option
		The description can also start on the next line.

		The description may contain multiple body elements,
		regardless of where it starts.

  -x, -y, -z    Multiple options are an "option group".
  -v, --verbose  Commonly-seen: short & long options.
  -1 file, --one=file, --two file
		Multiple options with arguments.
  /V            DOS/VMS-style options too

  There must be at least two spaces between the option and the
  description.

.. class:: tiny

::

  -a            command-line option "a"
  -b file       options can have arguments
		and long descriptions
  --long        options can be long also
  --input=file  long options can also have
		arguments

  --very-long-option
		The description can also start on the next line.

		The description may contain multiple body elements,
		regardless of where it starts.

  -x, -y, -z    Multiple options are an "option group".
  -v, --verbose  Commonly-seen: short & long options.
  -1 file, --one=file, --two file
		Multiple options with arguments.
  /V            DOS/VMS-style options too


  
Literal Blocks
--------------

Literal blocks are indicated with a double-colon ("::") at the end of
the preceding paragraph (over there ``-->``).  They can be indented::

    if literal_block:
        text = 'is left as-is'
        spaces_and_linebreaks = 'are preserved'
        markup_processing = None

Or they can be quoted without indentation::

>> Great idea!
>
> Why didn't I think of that?

------

::

  Literal blocks are indicated with a double-colon ("::") at the end of
  the preceding paragraph (over there ``-->``).  They can be indented::

      if literal_block:
	  text = 'is left as-is'
	  spaces_and_linebreaks = 'are preserved'
	  markup_processing = None

  Or they can be quoted without indentation::

  >> Great idea!
  >
  > Why didn't I think of that?
   
Line Blocks
-----------

| This is a line block.  It ends with a blank line.
|     Each new line begins with a vertical bar ("|").
|     Line breaks and initial indents are preserved.
| Continuation lines are wrapped portions of long lines;
  they begin with a space in place of the vertical bar.
|     The left edge of a continuation line need not be aligned with
  the left edge of the text above it.

| This is a second line block.
|
| Blank lines are permitted internally, but they must begin with a "|".

-------

::
   
  | This is a line block.  It ends with a blank line.
  |     Each new line begins with a vertical bar ("|").
  |     Line breaks and initial indents are preserved.
  | Continuation lines are wrapped portions of long lines;
    they begin with a space in place of the vertical bar.
  |     The left edge of a continuation line need not be aligned with
    the left edge of the text above it.

  | This is a second line block.
  |
  | Blank lines are permitted internally, but they must begin with a "|".
   
Block Quotes
------------

Block quotes consist of indented body elements:

    My theory by A. Elk.  Brackets Miss, brackets.  This theory goes
    as follows and begins now.  All brontosauruses are thin at one
    end, much much thicker in the middle and then thin again at the
    far end.  That is my theory, it is mine, and belongs to me and I
    own it, and what it is too.

    -- Anne Elk (Miss)

::

  Block quotes consist of indented body elements:

      My theory by A. Elk.  Brackets Miss, brackets.  This theory goes
      as follows and begins now.  All brontosauruses are thin at one
      end, much much thicker in the middle and then thin again at the
      far end.  That is my theory, it is mine, and belongs to me and I
      own it, and what it is too.

      -- Anne Elk (Miss)


Doctest Blocks
--------------

>>> print 'Python-specific usage examples; begun with ">>>"'
Python-specific usage examples; begun with ">>>"
>>> print '(cut and pasted from interactive Python sessions)'
(cut and pasted from interactive Python sessions)

----------

::

  >>> print 'Python-specific usage examples; begun with ">>>"'
  Python-specific usage examples; begun with ">>>"
  >>> print '(cut and pasted from interactive Python sessions)'
  (cut and pasted from interactive Python sessions)

Full tables
-----------

Here's a grid table followed by a simple table:

+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | Cells may span columns.          |
+------------------------+------------+---------------------+
| body row 3             | Cells may  | - Table cells       |
+------------------------+ span rows. | - contain           |
| body row 4             |            | - body elements.    |
+------------------------+------------+----------+----------+
| body row 5             | Cells may also be     |          |
|                        | empty: ``-->``        |          |
+------------------------+-----------------------+----------+

::

  +------------------------+------------+----------+----------+
  | Header row, column 1   | Header 2   | Header 3 | Header 4 |
  | (header rows optional) |            |          |          |
  +========================+============+==========+==========+
  | body row 1, column 1   | column 2   | column 3 | column 4 |
  +------------------------+------------+----------+----------+
  | body row 2             | Cells may span columns.          |
  +------------------------+------------+---------------------+
  | body row 3             | Cells may  | - Table cells       |
  +------------------------+ span rows. | - contain           |
  | body row 4             |            | - body elements.    |
  +------------------------+------------+----------+----------+
  | body row 5             | Cells may also be     |          |
  |                        | empty: ``-->``        |          |
  +------------------------+-----------------------+----------+

Simplified tables
-----------------

=====  =====  ======
   Inputs     Output
------------  ------
  A      B    A or B
=====  =====  ======
False  False  False
True   False  True
False  True   True
True   True   True
=====  =====  ======

::

  =====  =====  ======
     Inputs     Output
  ------------  ------
    A      B    A or B
  =====  =====  ======
  False  False  False
  True   False  True
  False  True   True
  True   True   True
  =====  =====  ======

Directives
==========

Directives
----------

These are just a sample of the many reStructuredText Directives.  For
others, please see
http://docutils.sourceforge.net/docs/ref/rst/directives.html.

Images
------

.. class:: tiny

  An image directive (also clickable -- a hyperlink reference):

  .. image:: logo-black.svg
     :width: 25%
     :target: http://example.com

  A figure directive:

  .. figure:: logo-black.svg
     :alt: reStructuredText, the markup syntax
     :width: 25%

     A figure is an image with a caption and/or a legend:

     +------------+-----------------------------------------------+
     | re         | Revised, revisited, based on 're' module.     |
     +------------+-----------------------------------------------+
     | Structured | Structure-enhanced text, structuredtext.      |
     +------------+-----------------------------------------------+
     | Text       | Well it is, isn't it?                         |
     +------------+-----------------------------------------------+

     This paragraph is also part of the legend.

.. class:: tiny

::

  An image directive (also clickable -- a hyperlink reference):

  .. image:: logo-black.svg
     :width: 25%
     :target: http://example.com

  A figure directive:

  .. figure:: logo-black.svg
     :alt: reStructuredText, the markup syntax
     :width: 25%

     A figure is an image with a caption and/or a legend:

     +------------+-----------------------------------------------+
     | re         | Revised, revisited, based on 're' module.     |
     +------------+-----------------------------------------------+
     | Structured | Structure-enhanced text, structuredtext.      |
     +------------+-----------------------------------------------+
     | Text       | Well it is, isn't it?                         |
     +------------+-----------------------------------------------+

     This paragraph is also part of the legend.

Admonitions
-----------

.. class:: tiny

  .. container::
       :class: column-50

    .. Attention:: Directives at large.

    .. Caution::

       Don't take any wooden nickels.

    .. DANGER:: Mad scientist at work!

    .. Error:: Does not compute.

    .. Hint:: It's bigger than a bread box.

  .. container::
       :class: column-50

    .. Important::
       - Wash behind your ears.
       - Clean up your room.
       - Call your mother.
       - Back up your data.

    .. Note:: This is a note.

    .. Tip:: 15% if the service is good.

    .. WARNING:: Strong prose may provoke extreme mental exertion.
       Reader discretion is strongly advised.

    .. admonition:: And, by the way...

       You can make up your own admonition too.

Admonitions
-----------

::

    .. Attention:: Directives at large.

    .. Caution::

       Don't take any wooden nickels.

    .. DANGER:: Mad scientist at work!

    .. Error:: Does not compute.

    .. Hint:: It's bigger than a bread box.

    .. Important::
       - Wash behind your ears.
       - Clean up your room.
       - Call your mother.
       - Back up your data.

    .. Note:: This is a note.

    .. Tip:: 15% if the service is good.

    .. WARNING:: Strong prose may provoke extreme mental exertion.
       Reader discretion is strongly advised.

    .. admonition:: And, by the way...

       You can make up your own admonition too.

Topics, Sidebars, and Rubrics
-----------------------------

.. sidebar:: Optional Sidebar Title
   :subtitle: Optional Subtitle

   This is a sidebar.  It is for text outside the flow of the main
   text.

   .. rubric:: This is a rubric inside a sidebar

   Sidebars often appears beside the main text with a border and
   background color.

.. topic:: Topic Title

   This is a topic.

.. rubric:: This is a rubric

Target Footnotes
----------------

.. target-notes::

Replacement Text
----------------

I recommend you try |Python|_.

.. |Python| replace:: Python, *the* best language around

Compound Paragraph
------------------

.. compound::

   This paragraph contains a literal block::

       Connecting... OK
       Transmitting data... OK
       Disconnecting... OK
      
   and thus consists of a simple paragraph, a literal block, and
   another simple paragraph.  Nonetheless it is semantically *one*
   paragraph.

This construct is called a *compound paragraph* and can be produced
with the "compound" directive.

Substitution Definitions
------------------------

An inline image (|example|) example:

::

  An inline image (|example|) example:

  .. |EXAMPLE| image:: images/biohazard.png

  (Substitution definitions are not visible in the HTML source.)

Comments
--------

Here's one:

.. Comments begin with two dots and a space. Anything may
   follow, except for the syntax of footnotes, hyperlink
   targets, directives, or substitution definitions.

-----------

::

  Here's one:

  .. Comments begin with two dots and a space. Anything may
     follow, except for the syntax of footnotes, hyperlink
     targets, directives, or substitution definitions.


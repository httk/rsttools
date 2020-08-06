========
rstslide
========

ReStructuredText (ReST) HTML slide generator for reveal.js
----------------------------------------------------------

**rstslide** is a fork of **rst2reveal** from https://github.com/vitay/rst2reveal

**rstslide** transforms reStructuredText (ReST) text files to HTML5 slides using the `Reveal.js <https://github.com/hakimel/reveal.js>`_ Javascript library developped by `Hakim El Hattab <http://hakim.se>`_. 

Dependencies
------------

In addition to Python 2.6 or 2.7 (not 3.x yet), **rstslide** requires the following packages:

* `docutils <http://docutils.sourceforge.net/>`_

* `setuptools <http://pypi.python.org/pypi/setuptools>`_

* `Reveal.js<https://github.com/hakimel/reveal.js>`_
  
If you want to display code in your slides, it is strongly advised to have `pygments <http://www.pygments.org>`_ installed for syntaxic color highlighting in many languages.

To directly generate plots within the ReST script, you will need `Matplotlib <http://matplotlib.org/>`_ (version >= 1.1) installed.

Installation
------------

Simply clone the git repository and run make::

    $ git clone https://github.com/rartino/rstslide.git
    $ cd rstslide
    $ make

and then add the `bin` directory to your path.
    
**rstslide** has been tested only on GNU/Linux systems, but perhaps it works on other platforms.

Usage
-----

You can go in the ``docs/`` subfolder and compile the presentation::
    
    cd docs/
    rstslide presentation.conf

Command-line options
--------------------
    
You can get a summary of command-line options by typing::

    rstslide --help

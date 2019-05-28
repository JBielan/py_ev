Lightweight poker library
=========================

py_ev is about to be a light-weight poker open-source library written
and tested in Python to help all programmers around the world build
their poker connected applications.

Installation
------------

.. code:: python

   pip install py_ev

Requirements
------------

-  ``Python 3.x``

Current functionalities
-----------------------

.. code:: python

   from py_ev import Evaluator

   ev = Evaluator()

-  Evaluator

   -  evaluate()

   .. code:: python

      print(ev.evaluate([(3, 3), (3, 2)], [(2, 2), (11, 3), (3, 4), (10, 2), (7, 3)]))
      # prints 4000420

   -  equity()

   .. code:: python

      print(ev.equity(100000, [(2, 3), (3, 2)], [(3, 3), (4, 2)]))
      # 100000 hands evaluated
      # prints (20.28, 30.8, 48.93)
      # Function returns a tuple: (cards_1_won, cards_2_won, draw)

Future development
------------------

Those are just examples of possible directions. Concrete decisions will
be made when some contributors join the project.

1. Adding the most popular poker variants: PLO, 6plus.
2. Hand history and tournaments summaries parsers.
3. Data extraction from poker operators (hhs-mining, traffic-mining,
   etc).
4. Sitting scripts.

Feel free to open a feature request.

How to join this project?
-------------------------

1. It’s as easy as clicking a “star” icon on the top. It really helps!
2. We are looking for contributors. If you feel like joining the ranks,
   read `THIS`_ article.

Every help is appreciated. No matter what your programming skills are.
You can: - improve README - write new testcases - document code with
Docstrings - **and of course write a new feature!**

Feel free to contact me privately on jkbielan@gmail.com

.. _THIS: https://gist.github.com/MarcDiethelm/7303312

.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
.. |Build Status| image:: https://travis-ci.org/JBielan/py_ev.svg?branch=master
   :target: https://travis-ci.org/JBielan/py_ev
.. |codecov| image:: https://codecov.io/gh/JBielan/py_ev/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/JBielan/py_ev
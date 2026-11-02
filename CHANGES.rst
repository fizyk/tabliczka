CHANGELOG
=========

.. towncrier release notes start

tabliczka 0.2.0 (2026-11-02)
============================

Breaking changes
----------------

- The learner's name is now given with ``--imie``, so ``tabliczka Ala dodawanie`` becomes ``tabliczka --imie Ala dodawanie``. Started without a name or a drill, the program asks for them. (`#3 <https://github.com/fizyk/tabliczka/issues/3>`__)


Features
--------

- Each release attaches a Windows program, ``tabliczka.exe``, that runs without installing Python. Typing ``koniec`` ends a drill, and the program's window stays open after the summary until a key is pressed. (`#2 <https://github.com/fizyk/tabliczka/issues/2>`__)


Miscellaneous
-------------

- Publish versioned releases with a changelog, built with uv_build and released with tbump and towncrier. (`#1 <https://github.com/fizyk/tabliczka/issues/1>`__)
- Check formatting, linting and typing with pre-commit, using ruff and ty. (`#11 <https://github.com/fizyk/tabliczka/issues/11>`__)

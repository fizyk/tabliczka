CHANGELOG
=========

.. towncrier release notes start

tabliczka 0.6.0 (2026-11-14)
============================

Features
--------

- The Windows program tells you when a newer version is out: at start it checks GitHub,
  and when there is one it names the version at the top of the window, with a link to
  its download page. It downloads nothing itself. With no internet connection, or when
  GitHub does not answer, the program works as before and says nothing. (`#39 <https://github.com/fizyk/tabliczka/issues/39>`__)


tabliczka 0.5.0 (2026-11-12)
============================

Features
--------

- The window remembers the name and the drill last started, separately for each Windows
  account, and shows them on the start page ready to change. On the first start no
  operations are chosen, so the child picks the ones they have learnt. The name and the
  drill are kept in ``profile.json`` in the account's ``AppData\Roaming\tabliczka``
  folder. (`#6 <https://github.com/fizyk/tabliczka/issues/6>`__)


Miscellaneous
-------------

- The code now uses the full name for the largest number; the program works as before. (`#32 <https://github.com/fizyk/tabliczka/issues/32>`__)
- The way the code is organised has changed; the program works as before. (`#33 <https://github.com/fizyk/tabliczka/issues/33>`__)


tabliczka 0.4.1 (2026-11-08)
============================

Miscellaneous
-------------

- The window was reorganised behind the scenes, ready for new drills; it works as
  before. (`#23 <https://github.com/fizyk/tabliczka/issues/23>`__)


tabliczka 0.4.0 (2026-11-07)
============================

Features
--------

- The Windows program is now a window instead of a console. It asks for the name and
  the drill (the operations, the largest number and the number of questions), then
  shows one question at a time: Enter checks the answer, the result shows in green or
  red, and the ``Koniec`` button shows the summary. An unexpected error shows in a
  message instead of closing the window. The command line stays for running from
  source. (`#5 <https://github.com/fizyk/tabliczka/issues/5>`__)


Miscellaneous
-------------

- Check the changelog with rstcheck without failing on the section headings each release repeats.


tabliczka 0.3.0 (2026-11-05)
============================

Features
--------

- Add the ``cwiczenie`` command, which drills any combination of addition,
  subtraction, multiplication and division chosen with ``--dzialanie``, all four by
  default. Every drill command takes ``--max``, the largest number (the sum for
  addition, the minuend for subtraction, each factor for multiplication and
  division), and ``--pytania``, the number of questions before the summary. Addition
  now defaults to a sum of at most 20, and subtraction to a minuend of at most 20.
  The summary shows each operation's wrong answers only when that operation has
  any. (`#4 <https://github.com/fizyk/tabliczka/issues/4>`__)


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

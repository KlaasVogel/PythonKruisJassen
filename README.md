# PythonKruisJassen
Generator for creating groups of 4 people where no one  plays another player more than once

# needed python modules:
numpy

First attempt was to slow and no sollutions could be found for 5 tables. Old code still available in the folder V1
trying to switch to a new way of solving this problem:
- wave form collapse with back tracing




V1 - slow and seems not to work for 5 tables (20 players)
    KJ_GUI is a GUI to view start/stop the "calculations"
    a grid (KruisGrid) is made and solved in KruisJassen.py
    logger.py is used to log info (for debugging)

    data is saved (after each 10k of steps done) in a json file: for resuming later.

    To start simply start KJ_GUI.py

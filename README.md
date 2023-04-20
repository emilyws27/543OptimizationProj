# 543OptimizationProj

This repository contains the code and output for the three algorithms developed in this [report](https://docs.google.com/document/d/1ZW3uADwB4MCw09cmJ-SFkfP8_w5HovIHfPX7dCnO020/edit?usp=sharing)

Authored by Emily Sheehan, Jack Heuberger, Jake Browning, and Nick Crispino for Washington University in St. Louis's class, CSE 543T, Algorithms for Non-linear Optimization.


## Usage

**main.py** contains all of the algorithms and helper methods to re-create the results.

The methods that you will call are the first 3 methods in the file; **identical_machines**, **uniform_machines**, and **schedule_with_dependencies**. The names are self explanatory as to which scheduling procedure they implement, and I refer you to the method comments as to what arguments they take and what they return.

Currently, 20 processors, 200 tasks, and a large number of dependencies are encoded in the section at the bottom of **main.py** which aligns with the example scenario defined in the report. I refer you to the comments in that section as to how you should go about encoding your own scenario in order to get different results.

Simply run **main.py** to see the results, they will be printed to the console. For larger applications, one could update this code to save the results to disk, but that is not necessary for our application.

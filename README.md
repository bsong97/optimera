Optimera
========

A repository that stores and shows some of the optimization problems

It requires the Coopr package (not included) which contains the Pyomo (Python Optimization Modeling Object) library. The Coopr package calls the GLPK solver to solve the LP problem.

Currently with the following problem:

wyndor
------
A simple LP problem that optimizes the profit from a plant which produces windows and doors. 


hansen
------
A clone of wyndor that optimizes the profit from a fruit juice plant that produces different types of fruit juices. 


farming
-------
LP problem: A farmer has a piece of land to be planted of Z km2 with barley, wheat, rice, maize, or their different combinations. The farmer has a limited amount of fertilizer, F kilograms, and insecticide, P kilograms.

Every km2 of barley requires F1 kg of fertilizer, P1 kg of insecticide
Every km2 of wheat requires F2 kg of fertilizer, P2 kg of insecticide
Every km2 of rice requires F3 kg of fertilizer, P3 kg of insecticide
Every km2 of maize requires F4 kg of fertilizer, P4 kg of insecticide

Let S1 be selling price of barley per km2
Let S2 be selling price of wheat per km2
Let S3 be selling price of rice per km2
Let S4 be selling price of maize per km2

We denote the area of planted with barley, wheat, rice and maize as x1, x2, x3, x4

The revenue can be maximized by choosing optimal values for x1, x2, x3 and x4.
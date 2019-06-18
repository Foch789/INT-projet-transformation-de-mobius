# Slam extension
Internship in Institute of Neuroscience of la Timone for my computer licence

[![Build Status](https://travis-ci.com/Foch789/INT-projet-transformation-de-mobius.svg?branch=master)](https://travis-ci.com/Foch789/INT-projet-transformation-de-mobius)
[![Coverage Status](https://coveralls.io/repos/github/Foch789/INT-projet-transformation-de-mobius/badge.svg?branch=master)](https://coveralls.io/github/Foch789/INT-projet-transformation-de-mobius?branch=master)

**Project :  Transformation de Mobius**

The objectif of project is to reduce the distortion in general when you transform a model to sphere.
For this, we use mobius transformation to allow that and we compute the distortions to see the improve.

This is a extension of project in python: [Slam project](https://github.com/gauzias/slam).

## Required

This project need :

  - [Slam project](https://github.com/gauzias/slam)

  - [MoebiusRegistration](https://github.com/mkazhdan/MoebiusRegistration) (If the makefile doesn't work. Try to repalce their makefile by my makefile in "The makefile for MoebiusRegistration")

  - [Trimesh](https://github.com/mikedh/trimesh)

## Provided

Also try example scripts located in "slam_extension/examples" folder.
We provide 3 models (2 foetus and 1 brain model with ply extension).
Also I give you the executables files of project MoebiusRegistration (Windows / Linux).

## Explanation of the 3 files

  - compare model: Multiple functions to allow comparison by several models. (Display the distortions differences between the first model and them)

  - stereo_projection File provided by Guillaume Auzias (internship supervisor) : Make stereographic projections

  - transformation_sphere : Make a transformation on the complex plan thank to Moebius Transformation  that aims to reduce distortions (See one example in folder "examples/mobius_transformation_evolution")

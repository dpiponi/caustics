Caustics
========
Code to render plots of functions modelling caustics with diffraction.

Status
------
This is pretty much complete. The goal was to compute certain integrals for a certain range of parameters and the code does so.

Compare this plot of the Pearcey integral generated using pearcey.py:
![Plot of absolute value of Pearcey function](Plot_of_absolute_value_of_Pearcey_integral.png?raw=true)

with this photograph of a caustic created by illuminating the bathroom wall with a laser pointer through a drop of water on the mirror:

![Photograph of a cusp caustic](A_photograph_of_a_cusp_caustic.png?raw=true)

Here's the hyperbolic-umbilic caustic:
![Plot of absolute value of Hyperbolic-Umbilic function](Plot_of_absolute_value_of_hyperbolic_umbilic_integral.png?raw=true)

For definitions, see http://dlmf.nist.gov/36.2

Some plots are 2D. These produce just a single image in a matplotlib window.

Some plots are 3D. These output a sequence of images that should be viewed as an animation.

One way to make an animation is to use the following:

    convert *.png out.gif
    convert out.gif -coalesce -duplicate 1,-2-1 -quiet -layers OptimizePlus -loop 0 new.gif

(Make sure you clear out any old .png files before you start rendering the new ones.)

I have also added some GLSL code. This is used at [Shadertoy](https://www.shadertoy.com/view/ltlyzj).

The images produced by my code disagreed with those at the NIST web site.
Turns out my code was correct: http://dlmf.nist.gov/errata/

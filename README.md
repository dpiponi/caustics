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

A Note On The Integration
-------------------------
There's a trick I use to compute the integrals of oscillatory functions.
If you want to integrate exp(if(x)) and f is analytic then you can deform the integration contour from the real line without changing the integral.
The oscillations come from the real part of f but the size of the oscillations is determined by the imaginary part of f.
So we should deform to a contour that increases Im f(z).
(Because |exp(i i d)| < 1 if d > 0.)
I do that by computing the gradient of Im f(z) and deforming the gradient in that direction.
Contour integration is frequently used for theoretical analysis of integrals like these but I've rarely seen it used for
numerical methods, especially with a numerically determined contour.
Caveat: as f gets more complicated it gets harder to guarantee you're taking a step in a good direction, even if you're using the
gradient to guide you, so you have to take a smaller step.
So in practice you need to fiddle about with the numbers a bit to get good results and in one case I modified the method significantly.
(Note you have a vast amount of freedom here because of Cacuchy's integral theorem.)
Future work: I think there may be a nice iterative method like gradient descent to find a good contour.

The Code
--------

Some plots are 2D. These produce just a single image in a matplotlib window.

Some plots are 3D. These output a sequence of images that should be viewed as an animation.

One way to make an animation is to use the following:

    convert *.png out.gif
    convert out.gif -coalesce -duplicate 1,-2-1 -quiet -layers OptimizePlus -loop 0 new.gif

(Make sure you clear out any old .png files before you start rendering the new ones.)

I have also added some GLSL code. This is used at [Shadertoy](https://www.shadertoy.com/view/ltlyzj).

The images produced by my code disagreed with those at the NIST web site.
Turns out my code was correct: http://dlmf.nist.gov/errata/

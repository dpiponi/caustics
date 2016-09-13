Code to render plots of functions modelling caustics with diffraction.

For definitions, see http://dlmf.nist.gov/36.2

Some plots are 2D. These produce just a single image in a matplotlib window.

Some plots are 3D. These output a sequence of images that should be viewed as an animation.

One way to make an animation is to use the following:

    convert *.png out.gif
    convert out.gif -coalesce -duplicate 1,-2-1 -quiet -layers OptimizePlus -loop 0 new.gif

(Make sure you clear out any old .png files before you start rendering the new ones.)

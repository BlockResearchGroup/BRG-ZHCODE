# Support for nurbs curves and surfaces through OCC with an API similar to Rhino's...
# Explore the various constructors and the attrobutes of the objects.
# Also explore again the link between the parametric definition and the discrete representations.

from compas.geometry import Box
from compas.geometry import NurbsCurve
from compas.geometry import Point
from compas_viewer.viewer import Viewer

box = Box(xsize=3, ysize=2, zsize=1)

points = []

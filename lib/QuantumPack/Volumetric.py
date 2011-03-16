#
# Types package
#

import sys
import string
import math
import numpy
from QuantumPack.Types import *
from QuantumPack.Geometry import *

# TODO: verbose
class Volumetric(Geometry):
  def __init__( self, name = "" ):
    Geometry.__init__( name )
    self.voldata = {}
  # end def

# end class Volumetric

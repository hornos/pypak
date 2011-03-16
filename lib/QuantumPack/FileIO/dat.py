#
# IO Package
# TAB: 4
#
import os
import sys
import math
import string
import numpy

from QuantumPack.File     import File
from QuantumPack.Types    import *
from QuantumPack.Geometry import Geometry

# UPOT has a fixed format check unified/upot.F

class FileIO( File ):
  def __init__( self, path = None, opts = "", sysopts = { "verbose" : False, "debug" : False } ):
    File.__init__( self, path, opts, sysopts )
  # end def


  def read_np( self ):
    np = self.line()[0]
    self.np  = string.atoi( np )
    self.dat = numpy.zeros(self.np)
  # end def


  def read_points( self ):
    for i in range( 1, self.np + 1 ):
      if i > 1:
        self.getline()
      # end if
      (x,y) = self.line()
      x = string.atof( x )
      y = string.atof( y )
      self.dat[i-1] = y
      self.process()
    # end for
  # end def


  def read( self, opts = None ):
    self.rewind()
    self.clean()
    self.state( 4, self.read_np )
    File.run( self, 4 )
    self.state( 5, self.read_points )
    File.run( self,5 )
  # end def


  def average( self, argv = None ):
    avg = 0.000
    for i in range( 1, self.np + 1 ):
      avg += self.dat[i-1]
    # end for
    return avg / self.np
  # end def

# end class

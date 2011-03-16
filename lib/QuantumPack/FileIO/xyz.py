#
# IO Package
# TAB: 4
#
import os
import sys
import string
import numpy

from QuantumPack.File     import File
from QuantumPack.Types    import *
from QuantumPack.Geometry import Geometry

class FileIO( File ):
  def __init__( self, path = None, opts = "", sysopts = { "verbose" : False, "debug" : False } ):
    File.__init__( self, path, opts, sysopts )
    self.geom = Geometry( 'xyz' )
    self.species = {}
  # end def

  ### begin write
  def write( self, opts = None ):
    line1 = ""
    line2 = ""
    self.rewind()
    self.clean()
    # dump header
    self.putline( self.geom.number_of_atoms() )
    self.putline( self.geom.name )
    # dump coordinates
    for a in self.geom.atoms:
      s = a.symbol()
      pos = a.position()
      mov = a.moveable()
      line1 = "  %2s" % s
      for i in range( 0, 3 ):
        line1 += "  %20.16f" % pos[i]
      # end for
      self.putline( line1 )
    # end for
    #
    self.buffer_write()
  # end def
  ### end write
# end class

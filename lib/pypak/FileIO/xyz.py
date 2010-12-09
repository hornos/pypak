#
# IO Package
# TAB: 4
#
import os
import sys
import string
import numpy

from pypak.File     import File
from pypak.Types    import *
from pypak.Geometry import Geometry

class FileIO( File ):
  def __init__( self, path = None, opts = "", sysopts = { "verbose" : False, "debug" : False } ):
    File.__init__( self, path, opts, sysopts )
    self.geom = Geometry( 'xyz' )
    self.species = {}
  # end def

  def read( self, opts = None ):
    raise NotImplementedError( "read" )
  # end def

  ### begin write
  def write( self, opts = None ):
    line = ["",""]
    self.rewind()
    self.clean()
    # dump header
    self.putline( self.geom.natoms() )
    self.putline( self.geom.name )
    # dump coordinates
    for atom in self.geom.atoms:
      s = atom.symbol
      pos = atom.position
      mov = atom.moveable
      line[0] = "  %2s" % s
      for i in range( 0, 3 ):
        line[0] += "  %20.16f" % pos[i]
      # end for
      self.putline( line[0] )
    # end for
    #
    self.write_buffer()
  # end def
  ### end write
# end class

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
    self.geom = Geometry( 'SCCOUT' )
    self.species = {}
  # end def

#  def read_lattice_vectors( self ):
#    for i in range( 1, 4 ):
#      if i > 1:
#        self.getline()
#      # end if
#      line_arr = self.line.split()
#      for j in range( 0, 3 ):
#        self.geom.lattice_vectors[i-1][j] = string.atof(line_arr[j])
#      # end for
#      self.process()
#    # end for
#  # end def

  def read_positions( self ):
    i = 1
    while True:
      if i > 1:
        try:
          self.getline()
        except:
          break
        # end try
      # end if
      ( no, x, y, z, r ) = self.line()
      x = string.atof( x )
      y = string.atof( y )
      z = string.atof( z )
      s = self.dict['global_specie']
      atom = AtomPosition( Atom( s, i ), VectorPosition( [ x, y, z ] ) )
      # atom.info()
      self.geom.add_atom( atom )
      self.process()
      i += 1
    # end for

    self.geom.position_type = PositionTypes.Cart
  # end def

  def read( self, opts = None ):
    self.rewind()
    self.clean()
    self.state( 2, self.read_lattice_vectors )
    File.run( self, 2 )

    # self.state( 25, self.read_positions )

    self.state( 29, self.read_positions )
    # self.state( 31, self.read_positions )
    File.run( self )
    self.geom.gen_species()
    #self.geom.check()
  # end def

# end class

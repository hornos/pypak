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
    self.geom = Geometry( 'POSCAR' )
    self.species = {}
    self.voldata = {}
  # end def


  ### begin read
  def read_lattice_constant( self ):
    constant = self.line()[0]
    self.geom.lattice_constant = string.atof( constant )
    self.process()
    self.species = {}
  # end def

  def read_types( self ):
    line_arr_1 = self.line()
    self.process()

    self.getline()
    line_arr_2 = self.line()
    self.process()

    for i in range( 0, len( line_arr_1 ) ):
      self.species[line_arr_1[i]] = string.atoi( line_arr_2[i] )
    # end for
    # print self.species
  # end def

  def read_position_type( self ):
    if string.upper( self.line()[0][0] ) == 'D':
      self.geom.position_type = PositionTypes.Direct
    else:
      self.geom.position_type = PositionTypes.Cart
    # end if
    self.process()
  # end def

  # old version
  def read_positions( self ):
    j = 1
    for s in self.species:
      for i in range( 0, self.species[s] ):
        if j > 1:
          self.getline()
        # end if
        # POSCAR or CHGCAR
        try:
          ( x, y, z, xm, ym, zm ) = self.line()
        except:
          ( x, y, z ) = self.line()
          xm = ym = zm = 'T'
        # end try
        x = string.atof( x )
        y = string.atof( y )
        z = string.atof( z )
        atom = AtomPosition( Atom( s, j ), VectorPosition( [ x, y, z ], [ xm, ym, zm ] ) )
        # atom.info()
        self.geom.add_atom( atom )
        if self.verbose:
          print " %05d Process:" % self.lc(), "%4d" % j, "%3d" % i, "%2s" % s, self.line()
        # end if
        j += 1
      # end for
    # end for
  # end def

  # converter version
  # do not need to convert at read
  def new_bad_read_positions( self, position_type = PositionTypes.Direct ):
    j = 1
    for s in self.species:
      for i in range( 0, self.species[s] ):
        if j > 1:
          self.getline()
        # end if
        try:
          ( x, y, z, xm, ym, zm ) = self.line()
        except:
          ( x, y, z ) = self.line()
          xm = ym = zm = 'T'
        # end try
        x = string.atof( x )
        y = string.atof( y )
        z = string.atof( z )
        pos = numpy.zeros( 3 )
        convert = 'O'
        # convert
        if self.geom.position_type != position_type:
          if position_type == PositionTypes.Cart:
            # D -> C
            convert = 'D->C'
            rho = numpy.array( [ x, y, z ] )
            pos = self.geom.position_cart( rho )
          else:
            # C -> D
            convert = 'C->D'
            r   = numpy.array( [ x, y, z ] )
            pos = self.geom.position_direct( r )
          # end if
        else:
          pos = numpy.array( [x, y, z ] )
        # end if
        
        # atom = AtomPosition( Atom( s, j ), VectorPosition( [ x, y, z ], [ xm, ym, zm ] ) )
        atom = AtomPosition( Atom( s, j ), VectorPosition( pos, numpy.array( [ xm, ym, zm ] ) ) )

        # print [x,y,z]
        # print pos
        # atom.info()
        self.geom.add_atom( atom )
        if self.verbose:
          print " %05d Process:" % self.lc(), "%4d" % j, "%3d" % i, "%2s" % s, self.line(), "%5s" % convert
        # end if
        j += 1
      # end for
    # end for
  # end def

  def read( self, opts = None ):
    self.rewind()
    self.clean()
    self.state( 1, self.comment )
    self.state( 2, self.read_lattice_constant )
    self.state( 3, self.read_lattice_vectors )
    File.run( self, 3 )
    self.state( 6, self.read_types )
    self.state( 8, self.comment )
    self.state( 9, self.read_position_type )
    # self.state( 8, self.read_position_type )
    self.state( 10, self.read_positions )
    File.run( self )
    self.geom.gen_species()
    self.geom.check()
  # end def
  ###  end read

  ### begin write
  # here we need to convert
  def write( self, opts = None ):
    line1 = ""
    line2 = ""
    self.rewind()
    self.clean()
    # dump header
    self.putline( self.geom.name )
    # dump lattice
    self.putline( "  %20.16f" % self.geom.lattice_constant )
    for i in range( 0, 3 ):
      line1 = ""
      for j in range( 0, 3 ):
        line1 += "  %20.16f" % self.geom.lattice_vectors[i][j]
      # end for
      self.putline( line1 )
    # end for
    # dump species
    line1 = ""
    line2 = ""
    for s in self.geom.species:
      line1 += "  %4s" % s
      line2 += "  %4d" % self.geom.species[s]
    # end for
    self.putline( line1 )
    self.putline( line2 )
    # dump coordinates
    self.putline( 'Selective dynamics' )
    try:
      position_type = opts['position_type']
    except:
      position_type = PositionTypes.Direct
    # end try
    # self.putline( PositionTypesDict[ self.geom.position_type ] )
    self.putline( PositionTypesDict[ position_type ] )

    # print self.geom.position_type
    # print position_type

    if self.verbose:
      print " Conversion:", "%s to %s" % ( PositionTypesDict[ self.geom.position_type ], PositionTypesDict[ position_type ] )
    # end if

    for a in self.geom.atoms:
      line1 = ""
      line2 = ""
      # convert
      if self.geom.position_type != position_type:
        if position_type == PositionTypes.Cart:
          # D -> C
          opos = a.position()
          pos = self.geom.position_cart( a.position() )
        else:
          # C -> D
          pos = self.geom.position_direct( a.position() )
        # end if
      else:
        pos = a.position()
      # end if

      mov = a.moveable()
      for i in range( 0, 3 ):
        line1 += "  %20.16f" % pos[i]
        line2 += "  %2s" % TF( mov[i] )
      # end for
      line1 += line2
      self.putline( line1 )
    # end for
    #
    self.putline( "" )
    
    for a in self.geom.atoms:
      line1 = ""
      vel = a.velocity()
      for i in range( 0, 3 ):
        line1 += "  %20.16f" % vel[i]
      # end for
      self.putline( line1 )
    # end for
    # print self.buffer.lines
    
    self.buffer_write()
  # end def
  ### end write
# end class

#
# IO Package
# TAB: 4
#
import os
import sys
import string
import numpy

from pypak.Types    import *
from pypak.IO.File  import File
from pypak.Geometry import Geometry

class IO( File ):
  def __init__( self, path = None, opts = "", sysopts = { "verbose" : False, "debug" : False } ):
    File.__init__( self, path, opts, sysopts )
    self.geom = Geometry( 'POSCAR' )
    self.species = {}
  # end def

  def read( self, opts = None ):
    self.rewind()
    self.clean()
    self.state( 1,  self.read_name )
    self.state( 2,  self.read_lat_c )
    self.state( 3,  self.read_lat_vec )
    File.run( self, 3 )
    self.state( 6,  self.read_types )
    self.state( 8,  self.comment )
    self.state( 9,  self.read_pt )
    self.state( 10, self.read_positions )
    File.run( self )
    self.geom.gen_species()
    # self.geom.info()
  # end def
  ###  end read

  def read_name( self ):
    self.geom.name = ''.join( self.line() )
  # end def

  ### begin read
  def read_lat_c( self ):
    constant = self.line()[0]
    self.geom.lat_c = string.atof( constant )
    self.process()
  # end def

  # super: read.lat_vec

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

  def read_pt( self ):
    if string.upper( self.line()[0][0] ) == 'D':
      self.geom.pt = PT.Direct
    else:
      self.geom.pt = PT.Cart
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
        self.geom.add( AtomPos( symbol = s, no = j, 
                                vec = [ x, y, z ], 
                                moveable = [ xm, ym, zm ] ) )
        if self.debug:
          print " %05d Process:" % self.lc(), "%4d" % j, "%3d" % i, "%2s" % s, self.line()
        # end if
        j += 1
      # end for
    # end for
  # end def


  ### begin write
  # here we need to convert
  def write( self, opts = None ):
    line = ["",""]
    self.rewind()
    self.clean()
    # dump header
    self.putline( self.geom.name )
    # dump lattice
    self.putline( "  %20.16f" % self.geom.lat_c )
    for i in range( 0, 3 ):
      line[0] = ""
      for j in range( 0, 3 ):
        line[0] += "  %20.16f" % self.geom.lat_vec[i][j]
      # end for
      self.putline( line[0] )
    # end for
    # dump species
    line = ["",""]
    for s in self.geom.species:
      line[0] += "  %4s" % s
      line[1] += "  %4d" % self.geom.species[s]
    # end for
    self.putline( line[0] )
    self.putline( line[1] )
    # dump coordinates
    self.putline( 'Selective dynamics' )
    try:
      pt = opts['pt']
    except:
      pt = PT.Direct
    # end try
    self.putline( PTD[ pt ] )

    if self.verbose:
      print " Conversion:", "%s to %s" % ( PTD[ self.geom.pt ], PTD[ pt ] )
    # end if

    for atom in self.geom.atoms:
      line = ["",""]
      # convert
      pos = atom.position
      if self.geom.pt != pt:
        if pt == PT.Cart:
          # D -> C
          opos = atom.position
          pos = self.geom.position_cart( atom.position )
        else:
          # C -> D
          pos = self.geom.position_direct( atom.position )
        # end if
      # end if

      mov = atom.moveable
      for i in range( 0, 3 ):
        line[0] += "  %20.16f" % pos[i]
        line[1] += "  %2s" % TF( mov[i] )
      # end for
      line[0] += line[1]
      self.putline( line[0] )
    # end for
    #
    self.putline( "" )

    for atom in self.geom.atoms:
      line = ""
      vel = atom.velocity
      for i in range( 0, 3 ):
        line += "  %20.16f" % vel[i]
      # end for
      self.putline( line )
    # end for

    self.write_buffer()
  # end def
  ### end write
# end class

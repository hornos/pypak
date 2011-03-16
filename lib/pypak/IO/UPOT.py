#
# IO Package
# TAB: 4
#
import os
import sys
import math
import string
import numpy

from pypak.Types         import *
from pypak.IO.IO         import IO
from pypak.IO.File       import File
from pypak.Geometry      import Geometry
from pypak.Math          import *

class IO( File ):
  def __init__( self, path = None, opts = "", sysopts = { "verbose" : False, "debug" : False } ):
    File.__init__( self, path, opts, sysopts )
    self.geom = Geometry( 'UPOT' )
    self.reference = None
  # end def

  def read( self, opts = None ):
    self.rewind()
    self.clean()
    self.state( 1, self.comment )
    self.state( 2, self.read_types_header )
    self.state( 3, self.comment )
    self.state( 4, self.read_types )
    File.run( self, 4 )
    self.state( 4 + self.types, self.comment )
    self.state( 4 + self.types + 2, self.comment )
    self.state( 4 + self.types + 3, self.read_ions )
    File.run( self )
    self.geom.gen_species()
    # self.geom.check()
  # end def

  def read_types_header( self ):
    (types,ions) = self.line()
    self.types = string.atoi( types )
    self.ions  = string.atoi( ions )
    self.process()
  # end def

  def read_types( self ):
    for i in range( 1, self.types + 1 ):
      if i > 1:
        self.getline()
      # end if
      self.process()
    # end for
  # end def

  def read_ions( self ):
    for i in range( 1, self.ions + 1 ):
      if i > 1:
        self.getline()
      # end if
      (no,symbol,cl_shift,x,y,z) = self.line()
      no = string.atoi( no )
      cl_shift = string.atof( cl_shift )
      x = string.atof( x )
      y = string.atof( y )
      z = string.atof( z )
      try:
        self.geom.add( AtomPos( symbol, no, cl_shift, numpy.array( [x, y, z] ) ) )
      except Exception as ex:
        print str( ex )
      # end try
      self.process()
    # end for
  # end def


  def average_upot( self, argv = None ):
    atomlist = argv['atomlist']
    ref      = argv['reference']
    vacancy  = argv['vacancy']
    spec = {}
    avg_cl_shift = 0.000

    # lattice vectors
    try:
      lat_vec = argv['lat_vec']
      self.geom.lat_vec = numpy.reshape( lat_vec, ( 3, 3 ) )
      if ref != None:
        ref.geom.lat_vec = numpy.reshape( lat_vec, ( 3, 3 ) )
      # end if
      msg = PTD[PT.Cart]
      # cart origo?
      try:
        origo_vec = argv['origo_vec']
      except:
        origo_vec = None
      # end try
    # end if
    except:
      lat_vec = None
      msg = PTD[PT.Direct]
    # end try
    if self.verbose:
      print " Coords:",msg
    # end if

    if lat_vec != None:
      avg_xyz = Geometry()
      avg_xyz.lat_vec = self.geom.lat_vec
      avg_xyz.pt = PT.Cart
    # end if

    if self.verbose:
      msg = "\n  %5s %4s %12s %12s %12s %12s" % ("No","Sym","cl_shift","x","y","z")
      if origo_vec != None:
        msg += " %12s" % ("dr")
        if ref != None:
          msg += " %12s" % ("ref dr")
      print msg
    # end if

    # cross check
    if ref != None:
      lookup = l_vacancy( range( 0, ref.geom.ac ), vacancy )
      ref_avg_cl_shift = 0.000
    # end if

    for ai in atomlist:
      atom = self.geom.get( ai )
      s    = atom.symbol
      no   = atom.no
      cls  = atom.cl_shift
      pos  = atom.position
      avg_cl_shift += cls

      # cross check
      if ref != None:
        ref_atom = ref.geom.get( lookup[ai] )
        ref_s    = ref_atom.symbol
        ref_pos  = ref_atom.position
        ref_cls  = ref_atom.cl_shift
        ref_avg_cl_shift += ref_cls
      # end if

      # cart position
      if lat_vec != None:
        # change to cart
        pos = self.geom.position( atom, PT.Cart )
        if ref != None:
          ref_pos = ref.geom.position( ref_atom, PT.Cart )
        avg_xyz.add( AtomPos( s, no, cls, pos ) )
      # end if

      if self.verbose:
        msg  = "  %5d %4s" % (atom.no, s)
        msg += " %12.6f" % cls
        msg += " %12.6f %12.6f %12.6f" % (pos[0], pos[1], pos[2])
        if origo_vec != None and lat_vec != None:
          msg += " %12.6f" % v_dr( origo_vec, pos )
        # end if
        print msg

        if ref != None:
          msg  = "R %5d %4s" % (ref_atom.no, ref_s)
          msg += " %12.6f" % ref_cls
          msg += " %12.6f %12.6f %12.6f" % (ref_pos[0], ref_pos[1], ref_pos[2])
          if origo_vec != None and lat_vec != None:
            msg += " %12.6f" % v_dr( origo_vec, ref_pos )
            msg += " %12.6f" % v_dr( ref_pos, pos )
          # end if
          print msg
        # end if
      # end if

      try:
        spec[s] += 1
      except:
        spec[s] = 1
      # end try
    # end for ai

    if self.verbose:
      print "\n Atoms: ", len( atomlist )
      print " Species: ", spec
      print "\n Orig. Average:", avg_cl_shift, "/", len( atomlist ), \
                        "=", avg_cl_shift / len( atomlist )
      if ref != None:
        print "  Ref. Average:", ref_avg_cl_shift, "/", len( atomlist ), \
                               "=", ref_avg_cl_shift / len( atomlist )
        print "\n Shift:", avg_cl_shift - ref_avg_cl_shift
      # end if

    # end if

    # end if
    if lat_vec != None:
      avg_output = IO( 'atomlist.xyz', 'xyz', 'w+' )
      avg_output.geom( avg_xyz )
      avg_output.write()
    # end if

    avg_cl_shift /= len( atomlist )
    return avg_cl_shift
  # end def



  def average( self, argv = None ):
    return self.average_upot( argv )
  # end def

# end class

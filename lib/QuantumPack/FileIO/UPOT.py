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
    self.geom = Geometry( 'UPOT' )
    self.reference_upot = None
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
        atom = Atom( symbol, no, cl_shift )
        vpos = VectorPosition( numpy.array( [x, y, z] ) )
        apos = AtomPosition( atom, vpos )
        self.geom.add_atom( apos )
      except Exception as ex:
        print str( ex )

#      self.geom.add_atom( AtomPosition( Atom( symbol, no, cl_shift ), VectorPosition( numpy.array( [x, y, z] ) ) ) )
      self.process()
    # end for
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


  def reference( self, argv = None ):
    reference_upot = argv['reference_upot']
    self.reference_upot = reference_upot
  # end def



# TODO: generate atomlist with origo rmin rmax
  def average_upot_on_reference( self, argv = None ):
    atomlist = argv['atomlist']
    if self.verbose:
      print
      print ' Average (reference):', atomlist
    avg_cl_shift = 0.000
    nat_cl_shift = 0.000
    reference_geom = self.reference_upot.geom()
    for i in atomlist:
      reference_atom = reference_geom.get_atom( i )
      nearest_atom = self.geom.nearest_atom_on_position( reference_atom.position() )
      nat_cl_shift = nearest_atom.cl_shift();
      if self.verbose:
        rp = reference_atom.position()
        np = nearest_atom.position()
        dp = np - rp
        dr = math.sqrt(dp[0]*dp[0]+dp[1]*dp[1]+dp[2]*dp[2])
        print
        print ' Reference:', "%3d" % reference_atom.no(), "%2s" % reference_atom.symbol(), rp
        print '   Nearest:', "%3d" % nearest_atom.no(), "%2s" % nearest_atom.symbol(), np
        print '  Distance:', dr
        print '  cl shift:', nat_cl_shift
        if reference_atom.symbol() != nearest_atom.symbol():
          print ' WARNING: Symbol mismatch'
        # end if
        if dr > 0.01:
          print ' WARNING: Distance to large'
        # end if
      # end if
      avg_cl_shift += nat_cl_shift
    # end for
    avg_cl_shift /= len( atomlist )
    return avg_cl_shift
  # end def


  def average_upot( self, argv = None ):
    atomlist = argv['atomlist']
    origo    = argv['origo']
    ref      = argv['reference']
    ono      = argv['ono']

    lv = argv['lv']
    if lv != None:
      self.geom.lattice_vectors = numpy.reshape(lv,(3,3))
      if ref != None:
        ref.geom.lattice_vectors = numpy.reshape(lv,(3,3))
    # end if

    # dump out atomlist xyz
    alout = open( './atomlist.xyz', 'w' )

    alout.write( str( len(atomlist) ) + "\n" )
    alout.write( "\n" )

    spec = {}
    if self.verbose:
      print
      print ' Average (self): ', atomlist
    avg_cl_shift = 0.000

    # self
    print "%5s %4s" % ("no", "sym"), "%12s %12s %12s" % ("x", "y", "z"), "%12s" % "cls", "%12s" % "dr"
    for i in atomlist:
      atom = self.geom.get_atom( i, True )
      cls  = atom.cl_shift()
      avg_cl_shift += cls

      s = atom.symbol()
      if lv != None:
        pos = self.geom.position( atom, PositionTypes.Cart )
        dr = 0.000
        for j in range(0,3):
          dr += (origo[j] - pos[j])**2
        # end for
        dr = math.sqrt(dr)
      else:
        pos = atom.position()
 
      print "%5d %4s" % (atom.no(), s), "%12.6f %12.6f %12.6f" % (pos[0], pos[1], pos[2]), "%12.6f" % cls, "%12.6f" % dr
      try:
        spec[s] += 1
      except:
        spec[s] = 1
      mov = atom.moveable()
      aline = "%2s" % s
      for j in range( 0, 3 ):
        aline += "  %20.16f" % pos[j]
      # end for
      alout.write( aline + "\n" )
    # end for
    alout.close()

    # reference cross-check
    if ref != None:
      ref_avg_cl_shift = 0.000
      print ""
      print "%5s %4s %4s" % ("no","sym","rsym"), "%12s %12s %12s" % ("dr","rdr", "ddr"), "%12s %12s %12s" % ("cls","rcls","dcls")

      sd_dcls = []

      for i in atomlist:
        atom = self.geom.get_atom( i, True )
        ii = i
        if ono != None:
          if i >= ono:
            ii = i + 1
            print ' Origo no shift: ',i,ii
        ref_atom = ref.geom.get_atom( ii, True )

        cls  = atom.cl_shift()
        ref_cls  = ref_atom.cl_shift()
        ref_avg_cl_shift += ref_cls

        s = atom.symbol()
        ref_s = ref_atom.symbol()

        sd_dcls.append( cls-ref_cls )

        if lv != None:
          pos = self.geom.position( atom, PositionTypes.Cart )
          ref_pos = self.geom.position( ref_atom, PositionTypes.Cart )

          dr = 0.000
          ref_dr = 0.000
          for j in range(0,3):
            dr += (origo[j] - pos[j])**2
            ref_dr += (origo[j] - ref_pos[j])**2
          # end for
          dr = math.sqrt(dr)
          ref_dr = math.sqrt(ref_dr)
        else:
          pos = atom.position()
          ref_pos = ref_atom.position()

        print "%5d %4s %4s" % (ref_atom.no(),s,ref_s), "%12.6f %12.6f %12.6f" % (dr,ref_dr,dr-ref_dr), "%12.6f %12.6f %12.6f" % (cls,ref_cls,cls-ref_cls)
      # end for
    # end if

    print ""
    print " Species: ", spec
    print ""
    print " Sum: ", avg_cl_shift," / ", len(atomlist)
    avg_cl_shift /= len( atomlist )

    if ref != None:
      ref_avg_cl_shift /= len(atomlist)
      print " Shift Mean: %12.6f" % (avg_cl_shift - ref_avg_cl_shift)
      print " Shift STD:  %12.6f" % numpy.std(sd_dcls)
    # end if
    
    return avg_cl_shift
    # print ' Average Potential: ' + str( avg_cl_shift )
  # end def


  def average( self, argv = None ):
    if self.reference_upot != None : 
      return self.average_upot_on_reference( argv )
    # end if
    return self.average_upot( argv )
  # end def

# end class

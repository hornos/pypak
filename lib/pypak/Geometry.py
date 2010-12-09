#
# Types package
#

import sys
import string
import math
import copy
import numpy
from pypak.Types import *

# TODO: verbose
class Geometry:
  def __init__( self, name = "" ):
    self.name    = name
    self.species = {}
    self.atoms   = []
    self.ac      = 0
    self.pt      = PT.Direct
    self.lat_vec = numpy.zeros((3, 3))
    self.rec_vec = numpy.zeros((3, 3))
    self.lat_c   = 1.0000 # Ang
  # end def

  def natoms( self ):
    return len( self.atoms )
  # end def

  def nspecies( self ):
    return len( self.species )
  # end def

  def info( self ):
    lv = self.lat_vec
    print "%20s%s" % ( "Name:", ' '+self.name )
    for i in range( 0, 3 ):
      print "%20s %9.6f %9.6f %9.6f" %( "a"+str(i+1)+":",lv[i][0], lv[i][1], lv[i][2] )
    # end for
    print "%20s%5d"  % ( "Species:", self.nspecies() )
    print "%20s%5d"  % ( "Atoms:", self.natoms() )
    print "%20s%5d"  % ( "PT:", self.pt )
    for atom in self.atoms:
      sym = atom.symbol
      no  = atom.no
      vec = atom.position
      print "%5s%5s%12.6f%12.6f%12.6f" % ( no, sym, vec[0], vec[1], vec[2] )
    # end for
  # end def

  def gen_species( self ):
    # reset
    self.species = {}
    # regenerate
    for atom in self.atoms:
      sym = atom.symbol
      try:
        self.species[sym] += 1
      except:
        self.species[sym] = 1
      # end try
    # end for
  # end def


  def add( self, atom = None, renum = False ):
    _atom = copy.deepcopy( atom )
    _atom.no = self.ac
    self.atoms.append( _atom )
    self.ac += 1
  # end def

  def get( self, i = 0, vmd = False ):
    if not vmd:
      return self.atoms[i-1]
    return self.atoms[i]
  # end def

  def order( self ):
    ordered = []
    for sym in self.species:
      for atom in self.atoms:
        if atom.symbol == sym:
          ordered.append( atom )
      # end for
    # end for
    self.atoms = ordered
  # end def

  def reciprocal( self ):
    self.rec_vec = numpy.linalg.inv( self.lat_vec )
  # end def


  def nearest_old( self, r = numpy.zeros(3) ):
    maxr  = 100000
    natom = None
    for a in self.atoms:
      d = a.position() - r
      dr = 0.000
      for i in range(0,3):
        dr += d[i]*d[i]
      # end for
      if maxr > dr:
        natom = a
        maxr  = dr
      # end if
    # end for
    return natom
  # end def

  def nearest( self, pos = None ):
    nearest_atom = None
    nearest_dpos = 100000.000
    for atom in self.atoms:
      dpos_vec = abs( numpy.subtract( atom.position(), pos ) )
      dpos_max = dpos_vec[ numpy.argmax( dpos_vec ) ]
      if dpos_max < nearest_dpos :
        nearest_atom = atom
        nearest_dpos = dpos_max
    # end for
    return nearest_atom
  # end def


  def position_direct( self, r = numpy.zeros( 3 ) ):
    self.reciprocal()
    rho = numpy.zeros( 3 )
    for i in range( 0, 3 ):
      for j in range( 0, 3 ):
        rho[i] += r[j] * self.rec_vec[j][i] / self.lat_c
      # end for
    # end for
    return rho
  # end def

  def position_cart( self, rho = numpy.zeros( 3 ) ):
    r = numpy.zeros( 3 )
    for i in range( 0, 3 ):
      for j in range( 0, 3 ):
        r[i] += rho[j] * self.lat_vec[j][i] * self.lat_c
      # end for
    # end for
    return r
  # end def

  def position( self, atom = None, pt = PT.Direct ):
    pos = r = atom.position()
    if self.pt != pt:
      if pt == PT.Cart:
        # D -> C
        pos = self.position_cart( r )
      else:
        # C -> D
        pos = self.position_direct( r )
      # end if
    # end if
    return pos
  # end def


  def cart( self ):
    # convert to cart
    if self.pt == PT.Direct:
      for atom in self.atoms:
        atom.position = self.position_cart( atom.position )
      # end for
      self.pt = PT.Cart
    # end if
  # end def

  def direct( self ):
    # convert to cart
    if self.pt == PT.Cart:
      for atom in self.atoms:
        atom.position = self.position_direct( atom.position )
      # end for 
      self.pt = PT.Direct
    # end if
  # end def

  def move( self, S = numpy.zeros( 3 ) ):
    for atom in self.atoms:
      atom.move( S )
    # end for
  # end def

# end class Geometry

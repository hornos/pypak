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

  def clone( self ):
    geom = Geometry( self.name )
    geom.species = copy.deepcopy( self.species )
    geom.atoms   = copy.deepcopy( self.atoms )
    geom.ac      = copy.deepcopy( self.ac )
    geom.pt      = copy.deepcopy( self.pt )
    geom.lat_vec = copy.deepcopy( self.lat_vec )
    geom.rec_vec = copy.deepcopy( self.rec_vec )
    geom.lat_c   = copy.deepcopy( self.lat_c )
    return geom
  # end if

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

    print "\n%5s%5s%12s%12s%12s" % ( "no", "sym", "x", "y", "z" )
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

  def get( self, i = 0, vmd = True ):
    if vmd:
      return self.atoms[i]
    return self.atoms[i-1]
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
    return numpy.dot( 1.0 / self.lat_c, numpy.dot( r, self.rec_vec ) )
  # end def

  def position_cart( self, rho = numpy.zeros( 3 ) ):
    return numpy.dot( self.lat_c, numpy.dot( rho, self.lat_vec ) )
  # end def

  def position( self, atom = None, pt = PT.Direct ):
    pos = r = atom.position
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

  def supercell( self, msc = numpy.zeros( [3, 3] ) ):
    vol = numpy.dot( msc[0,:], numpy.cross( msc[1,:], msc[2,:] ) )
    if not vol > 0.0:
      raise Exception( 'Not a right-hand system' )
    # end if
    # clone
    geom = self.clone()

    # scale lat_c
    if geom.lat_c != 1.0:
      geom.lat_vec = numpy.dot( geom.lat_c, geom.lat_vec )
    # end if
    # scale base
    geom.cart()

    sup_lat_vec = numpy.dot( msc, self.lat_vec )
    cmb = [[],[],[]]
    for i in range(0,3):
      mij = [0,0,0]
      lmn = [[],[],[]]
      for j in range(0,3):
        ij = msc[i][j]
        if ij < 0:
          mij[j] = ij
          lmn[j] = range(mij[j],0)
        else:
          mij[j] = ij + 1
          lmn[j] = range(1,mij[j])
        # end if
        if lmn[j] == []:
          lmn[j] = [0]
      # end for
      
      print lmn
      for l in lmn[0]:
        for m in lmn[1]:
          for n in lmn[2]:
            print i,l,m,n
            cmb[i] += [[l,m,n]]
          # end for
        # end for
      # end for
    # end for

    for o in cmb[0]:
      for p in cmb[1]:
        for q in cmb[2]:
          cmm = numpy.array([o,p,q])
          cmm_lat_vec = numpy.dot( cmm, self.lat_vec )
          print cmm_lat_vec
          # base transport
        # end for
      # end for
    # end for
    print len(cmb[0])*len(cmb[1])*len(cmb[2])
  # end def
# end class Geometry

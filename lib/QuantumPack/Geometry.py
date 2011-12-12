#
# Types package
#

import sys
import string
import math
# from Numeric import *
import copy
import numpy
from QuantumPack.Types import *

# TODO: verbose
class Geometry:
  def __init__( self, name = "" ):
    self.name    = name
    self.species = {}
    self.atoms   = []
    # atom counter
    # check !
    self.ac      = 0
    self.position_type    = PositionTypes.Direct
    self.lattice_vectors    = numpy.zeros( (3, 3) )
    self.reciprocal_vectors = numpy.zeros( (3, 3) )
    self.lattice_constant = 1.0000 # Angstrom
    self.lattice_unit     = 'Ang'
  # end def


  def number_of_atoms( self ):
    return len( self.atoms )
  # end def


  def number_of_species( self ):
    return len( self.species )
  # end def


  def check( self ):
    lv = self.lattice_vectors
    print "%20s%s" % ( "Name:", ' '+self.name )
    for i in range( 0, 3 ):
      print "%20s %9.6f %9.6f %9.6f" %( "a"+str(i+1)+":",lv[i][0], lv[i][1], lv[i][2] )
    # end for
    print "%20s%5d"  % ( "Species:", self.number_of_species() )
    print "%20s%5d"  % ( "Atoms:", self.number_of_atoms() )
    print "%20s%5d"  % ( "Pos. type:", self.position_type )
    for atom in self.atoms:
      sym = atom.symbol()
      no  = atom.no()
      vec = atom.position()
      print "%5s%5s%12.6f%12.6f%12.6f" % ( no, sym, vec[0], vec[1], vec[2] )
    # end for
  # end def


  def gen_species( self ):
    # reset
    self.species = {}
    # regenerate
    for atom in self.atoms:
      sym = atom.symbol()
      try:
        self.species[sym] += 1
      except:
        self.species[sym] = 1
      # end try
    # end for
    print self.species
  # end def


  def add_atom( self, atom = None, renum = False ):
    _atom = copy.deepcopy( atom )
    _atom.atom.no = self.ac
    self.atoms.append( _atom )
    self.ac += 1
  # end def


  def get_atom( self, i = 0, vmdindex = False ):
    if not vmdindex:
      return self.atoms[i-1]

    return self.atoms[i]
  # end def


  # TODO: do not need tolerance !
  def nearest_atom_on_position( self, pos = None ):
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


  def position( self, atom = None, position_type = PositionTypes.Direct ):
    pos = r = atom.position()
    R = numpy.zeros( 3 )

    if self.position_type != position_type:
      if position_type == PositionTypes.Cart:
        # D -> C
        pos = self.position_cart( r )
      else:
        # C -> D
        pos = self.position_direct( r )
      # end if
    # end if
    return pos
  # end def


  def position_shift( self, S = numpy.zeros( 3 ) ):
    for atom in self.atoms:
      for i in range( 0, 3 ):
        atom.pos.position[i] += S[i]
      # end for
    # end for
  # end def


  def merge( self, geom = None, check_position_type = True, check_lattice = True, tolerance = 0.00001 ):
    check_list = " Merge check:"

    # check position type
    if check_position_type and self.position_type != geom.position_type:
      raise Exception( 'position_type mismatch' )
    # end if
    check_list += " position_type"

    if check_lattice:
      if self.lattice_constant != geom.lattice_constant:
        raise Exception( 'lattice_constant mismatch' )
      # end if
      check_list += " lattice_constant"

      if self.lattice_unit != geom.lattice_unit:
        raise Exception( 'lattice_unit mismatch' )
      # end if
      check_list += " lattice_unit"

      for i in range( 0, 3 ):
        for j in range( 0, 3 ):
          if self.lattice_vectors[i][j] - geom.lattice_vectors[i][j] > tolerance:
            raise Exception( "lattice_vectors mismatch (%d,%d)" % (i,j) )
          # end if
        # end for
      # end for
      check_list += " lattice_vectors"
    # end if

    if not check_lattice:
      for i in range( 0, 3 ):
        for j in range( 0, 3 ):
          self.lattice_vectors[i][j] = geom.lattice_vectors[i][j]
    # end if

    # merge atoms
    for atom in geom.atoms:
      self.add_atom( copy.deepcopy( atom ), True )
    # end for

    # merge names
    self.name += ":" + geom.name 
    self.gen_species()
    return check_list
  # end def


  def clone( self, geom = None ):
    # self.name    = copy.deepcopy( geom.name )
    self.species = copy.deepcopy( geom.species )
    self.atoms   = copy.deepcopy( geom.atoms )
    self.ac      = copy.deepcopy( geom.ac )
    self.position_type      = copy.deepcopy( geom.position_type )
    self.lattice_vectors    = copy.deepcopy( geom.lattice_vectors )
    self.reciprocal_vectors = copy.deepcopy( geom.reciprocal_vectors )
    self.lattice_constant   = copy.deepcopy( geom.lattice_constant )
    self.lattice_unit       = copy.deepcopy( geom.lattice_unit )
  # end def


  def cart( self ):
    # convert to cart
    if self.position_type == PositionTypes.Direct:
      for atom in self.atoms:
        atom.position( self.position_cart( atom.position() ) )
      # end for
      self.position_type = PositionTypes.Cart
    # end if
  # end def


  def direct( self ):
    # convert to cart
    if self.position_type == PositionTypes.Cart:
      for atom in self.atoms:
        atom.position( self.position_direct( atom.position() ) )
      # end for 
      self.position_type = PositionTypes.Direct
    # end if
  # end def


  # TODO: always convert to cart
  def super( self, repeate = [] ):
    original_geom = Geometry( "Original" )
    original_geom.clone( self )

    # set lattice
    new_lattice_vectors = numpy.zeros( (3, 3) )
    for i in range( 0, 3 ):
      chi = repeate[i]
      xi  = chi[0] - chi[1]
      for j in range( 0, 3 ):
        new_lattice_vectors[i][j] = self.lattice_vectors[i][j] * xi
      # end for
    # end for

    # make supercell
    for l in range( repeate[0][0], repeate[0][1] + 1 ):
      for m in range( repeate[1][0], repeate[1][1] + 1 ):
        for n in range( repeate[2][0], repeate[2][1] + 1 ):
          if l == 0 and m == 0 and n == 0:
            continue
          # end if
          # shift_vector
          rho = numpy.array( [l, m, n] )
          S   = numpy.zeros( 3 )
          for i in range( 0, 3 ):
            for j in range( 0, 3 ):
              # S[j] += rho[i] * self.lattice_vectors[i][j] * self.lattice_constant
              S[i] += rho[j] * self.lattice_vectors[j][i] * self.lattice_constant
            # end for
          # end for
#          S = numpy.dot( rho, self.lattice_vectors )
          shift_geom = Geometry( "Shift" )
          shift_geom.clone( original_geom )
          shift_geom.position_shift( S )
          # shift_geom.check()
          self.merge( shift_geom, False, False )
        # end for
      # end for
    # end for

    self.name = "Supercell"
    # TODO: set super lattice vectors
    self.gen_species()
  # end def


  def order( self ):
    ordered = []
    for sym in self.species:
      for atom in self.atoms:
        if atom.symbol() == sym:
          ordered.append( atom )
      # end for
    # end for
    self.atoms = ordered
  # end def


  def reciprocal( self ):
    self.reciprocal_vectors = numpy.linalg.inv( self.lattice_vectors )
  # end def


  def position_direct( self, r = numpy.zeros( 3 ) ):
    self.reciprocal()
    rho = numpy.zeros( 3 )
    for i in range( 0, 3 ):
      for j in range( 0, 3 ):
        rho[i] += r[j] * self.reciprocal_vectors[j][i] / self.lattice_constant
      # end for
    # end for
    return rho
  # end def


  def position_cart( self, rho = numpy.zeros( 3 ) ):
    r = numpy.zeros( 3 )
    for i in range( 0, 3 ):
      for j in range( 0, 3 ):
        r[i] += rho[j] * self.lattice_vectors[j][i] * self.lattice_constant
      # end for
    # end for
    # print r
    # print rho
    return r
  # end def


  # TODO: not so ok
  def do_not_use_wignercell( self, origo = numpy.zeros(3), eps = 0.000000001 ):
    # reciprocal_vectors = numpy.linalg.inv( self.lattice_vectors )
    # print reciprocal_vectors
    # print self.lattice_vectors
    ordered = []
    ac = 0
    for atom in self.atoms:
      rho = numpy.zeros( 3 )
      r = atom.position()
      # TODO: refractor
      for i in range( 0, 3 ):
        for j in range( 0, 3 ):
          rho[i] += r[j] * reciprocal_vectors[j][i] / self.lattice_constant
        # end for
      # end for
      wigner = True
      for i in range( 0, 3 ):
        if abs( rho[i] ) < 0.500000000 - eps:
          wigner &= True
        else:
          wigner &= False
        # end if
      # end for
      # print wigner,atom.no(),atom.symbol(),rho

      if wigner:
        print atom.no(),atom.symbol(),rho
        ordered.append( atom )
        ac += 1
      # end if
    # end for
    print "Atoms: ",ac

    self.atoms = ordered
    self.gen_species()
  # end def


  def embed( self, embed_geom = None, embed_sym = None, embed_no = 0, input_sym = None, input_no = 0 ):
    # convert to cart
    self.cart()
    embed_geom.cart()

    # check
    atom = self.atoms[input_no]
    if atom.symbol() != input_sym:
      print ' Warning: symbol mismatch'

    embed_atom = embed_geom.atoms[embed_no]
    if embed_atom.symbol() != embed_sym:
      print ' Warning: symbol mismatch'

    # find closest from each origo
    origo = atom.position()
    embed_origo = embed_atom.position()

    closest = {}
    for a in embed_geom.atoms:
      r = a.position() - embed_origo + origo
      natom = self.nearest( r )
      # print '     R:', r
      # print '  Atom:', a.no(), a.symbol(), a.position() - embed_origo
      # print ' NAtom:', natom.no(), natom.symbol(), natom.position() - origo
      try:
        closest[a.no()]
        print ' Warining:', a.no()
      except:
        closest[a.no()] = natom.no()
      # end try
    # end for

    # print closest
    # check
    for embed_no,no in closest.iteritems():
      dr = 0.000
      embed_atom = embed_geom.atoms[embed_no]
      atom = self.atoms[no]
      d = embed_atom.position() - atom.position() - embed_origo + origo
      for i in range(0,3):
        dr += d[i]*d[i]
      # end for
      print ' Atom:',no,'-> NAtom:', embed_no, ' dR:', dr
      self.atoms[no].position( embed_atom.position() - embed_origo + origo )
      self.atoms[no].symbol( embed_atom.symbol() )
    # end for
    print ' Embed:', len(closest)
  # end def


  def nearest( self, r = numpy.zeros(3) ):
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


  def transform_mirror(self, shift = [], vmdindex = True ):
    i = shift[0]
    i = string.atoi(i)
    # xy: 2 xz: 1 yz: 0
    for atom in self.atoms:
      atom.pos.position[i] = -1.0 * atom.pos.position[i]
    # end for
    print " Mirror: ", i
  # end def

  def transform_rot(self, shift = [], vmdindex = True ):
    (a,b,c) = shift
    a = string.atof(a)*2.0*math.pi/180.0
    b = string.atof(b)*2.0*math.pi/180.0
    c = string.atof(c)*2.0*math.pi/180.0
    Rx = numpy.zeros((3,3))
    Ry = numpy.zeros((3,3))
    Rz = numpy.zeros((3,3))
    L  = numpy.zeros((3,3))
    R  = numpy.zeros((3,3))

    # x-axis
    Rx[0][0] = 1.0
    Rx[1][1] = math.cos(a)
    Rx[1][2] = -math.sin(a)
    Rx[2][1] = math.sin(a)
    Rx[2][2] = math.cos(a)

    # y-axis
    Ry[1][1] = 1.0
    Ry[0][0] = math.cos(b)
    Ry[0][2] = math.sin(b)
    Ry[2][0] = -math.sin(b)
    Ry[2][2] = math.cos(b)

    # z-axis
    Rz[2][2] = 1.0
    Rz[0][0] = math.cos(c)
    Rz[0][1] = -math.sin(c)
    Rz[1][0] = math.sin(c)
    Rz[1][1] = math.cos(c)

    for i in range(0,3):
      for j in range(0,3):
        L[i][j] = self.lattice_vectors[i][j]

    print "Rz"
    print Rz
    Rz = numpy.transpose(Rz)
    print "Original:"
    print self.lattice_vectors

    R = numpy.dot(L,Rz)
    for i in range(0,3):
      for j in range(0,3):
        self.lattice_vectors[i][j] = R[i][j]

    print "New:"
    print self.lattice_vectors
  # end def

  def transform_latrot(self, shift = [], vmdindex = True ):
    (deg, mir) = shift
    deg = string.atoi(deg)
    mir = string.atoi(mir)
    # rotated lattice
    L = numpy.zeros( (3,3) )

    deg = abs( deg % 4 )

    if deg == 1:
      for k in range(0,3):
        L[k][0] = self.lattice_vectors[k][1]
        L[k][1] = -1.000 * self.lattice_vectors[k][0]
      # end
      L[2][2] = self.lattice_vectors[2][2]
    elif deg == 2:
      for k in range(0,3):
        L[k][0] = -1.000 * self.lattice_vectors[k][0]
        L[k][1] = -1.000 * self.lattice_vectors[k][1]
      # end
      L[2][2] = self.lattice_vectors[2][2]
    elif deg == 3:
      for k in range(0,3):
        L[k][0] = -1.000 * self.lattice_vectors[k][1]
        L[k][1] = self.lattice_vectors[k][0]
      # end
      L[2][2] = self.lattice_vectors[2][2]
    else:
    # end
      for k in range(0,3):
        for l in range(0,3):
          L[k][l] = self.lattice_vectors[k][l]
        # end
      # end
    # end

    mir = abs( mir % 3 )
    for k in range(0,3):
      L[k][mir] = -1.000 * L[k][mir]
    # end

    print "Original"
    print self.lattice_vectors
    print "New"
    for k in range(0,3):
      for l in range(0,3):
        self.lattice_vectors[k][l] = L[k][l]
      # end
    # end
    print self.lattice_vectors
  # end def

  def transform_cshift(self, shift = [], vmdindex = True ):
    # (cx,cy,cz,sym,no) = shift
    (cx,cy,cz,deg,mir,sym,no) = shift

    # (no,sym,cx,cy,cz) = shift
    cx = string.atof(cx)
    cy = string.atof(cy)
    cz = string.atof(cz)
    deg = string.atoi(deg)
    mir = string.atoi(mir)
    no = string.atoi(no)
    c = numpy.array( [cx,cy,cz] )
    if not vmdindex:
      no -= 1
    # end if
    atom = self.atoms[no]
    if atom.symbol() != sym:
      print ' Warning: symbol mismatch'
    # shift vector
    S = numpy.zeros( 3 )

    # rotated lattice
    L = numpy.zeros( (3,3) )
    
    deg = abs( deg % 4 )

    if deg == 1:
      for k in range(0,3):
        L[k][0] = self.lattice_vectors[k][1]
        L[k][1] = -1.000 * self.lattice_vectors[k][0]
      # end
      L[2][2] = self.lattice_vectors[2][2]
    elif deg == 2:
      for k in range(0,3):
        L[k][0] = -1.000 * self.lattice_vectors[k][0]
        L[k][1] = -1.000 * self.lattice_vectors[k][1]
      # end
      L[2][2] = self.lattice_vectors[2][2]
    elif deg == 3:
      for k in range(0,3):
        L[k][0] = -1.000 * self.lattice_vectors[k][1]
        L[k][1] = self.lattice_vectors[k][0]
      # end
      L[2][2] = self.lattice_vectors[2][2]
    else:
    # end
      for k in range(0,3):
        for l in range(0,3):
          L[k][l] = self.lattice_vectors[k][l]
        # end
      # end
    # end

    if mir == 1:
      for k in range(0,3):
        L[k][1] = -1.000 * L[k][1]
      # end
    # end

    print self.lattice_vectors
    print L

    if self.position_type == PositionTypes.Direct:
      S = c
    else:
      for i in range( 0, 3 ):
        for j in range( 0, 3 ):
          # S[i] += c[j] * self.lattice_vectors[j][i] * self.lattice_constant
          # S[i] += c[j] * RL[j][i] * self.lattice_constant
          S[i] += c[j] * L[j][i] * self.lattice_constant
        # end for
      # end for
    # end if
    atom.shift( S )
    print ' Transform: shift', c, S, sym, no
  # end def

  # transfrom
  def transform_shift( self, shift = [], vmdindex = True ):
    (cx,cy,cz,sym,no) = shift
    # (no,sym,cx,cy,cz) = shift
    cx = string.atoi(cx)
    cy = string.atoi(cy)
    cz = string.atoi(cz)
    no = string.atoi(no)
    c = numpy.array( [cx,cy,cz] )
    if not vmdindex:
      no -= 1
    # end if
    atom = self.atoms[no]
    if atom.symbol() != sym:
      print ' Warning: symbol mismatch'
    # shift vector
    S = numpy.zeros( 3 )
    if self.position_type == PositionTypes.Direct:
      S = c
    else:
      for i in range( 0, 3 ):
        for j in range( 0, 3 ):
          S[i] += c[j] * self.lattice_vectors[j][i] * self.lattice_constant
        # end for
      # end for
    # end if
    # print atom.no(),atom.symbol(),S
    atom.shift( S )
    print ' Transform: shift', c, sym, no
  # end def


  def transform_rshift( self, shift = [] ):
    (cx,cy,cz,ax,op,lim) = shift
    cx = string.atoi(cx)
    cy = string.atoi(cy)
    cz = string.atoi(cz)
    lim = string.atof(lim)
    c = numpy.array( [cx,cy,cz] )
    # shift vector
    S = numpy.zeros( 3 )
    for i in range( 0, 3 ):
      for j in range( 0, 3 ):
        S[i] += c[j] * self.lattice_vectors[j][i] * self.lattice_constant
      # end for
    # end for
    axdict = {'x' : 0, 'y' : 1, 'z' : 2 }
    sc = 0
    self.cart()

    for atom in self.atoms:
      pos = atom.position()
      pax = pos[axdict[ax]]
      if op == "<":
        if pax < lim:
          atom.shift( S )
          print ' Transform: rshift',atom.no(),atom.symbol()
          sc = sc + 1
        # end if
      else:
        if pax > lim:
          atom.shift( S )
          print ' Transform: rshift',atom.no(),atom.symbol()
          sc = sc + 1
        # end if
      # end if
    # end for
    print ' Transform: rshift',ax,op,lim,' total:',sc
  # end def


  def transform_center( self, c = [], vmdindex = True ):
    # 0: no, 1: sym
    no  = string.atoi( c[0] )
    if not vmdindex:
      no -= 1
    # end if
    sym = c[1]
    atom = self.atoms[no]
    if atom.symbol() != sym:
      print ' Warning: symbol mismatch' 

    S = numpy.zeros(3)
    pos = atom.position()
    for i in range(0,3):
      S[i] = -pos[i]
    # end for
    # print S
    self.position_shift( S )
    #for atom in self.atoms:
    #  print atom.no(),atom.symbol(),atom.position()
    print ' Transform: center', S
  # end def

  def transform_vshift( self, c = [] ):
    S = numpy.zeros(3)
    for i in range(0,3):
      S[i] = string.atof( c[i] )
    # end for
    self.position_shift( S )
    print ' Transform: vshift'
  # end def

  # TODO: better cleaner names!
  def transform_lshift( self, c = [] ):
    rho = numpy.zeros(3)
    S   = numpy.zeros(3)
    for i in range(0,3):
      rho[i] = string.atof( c[i] )
    # end for
    for i in range( 0, 3 ):
      for j in range( 0, 3 ):
        S[i] += rho[j] * self.lattice_vectors[j][i] * self.lattice_constant
      # end for
    # end for
    self.position_shift( S )
    print ' Transform: lshift'
  # end def


  def transform_insert( self, c = [] ):
    for i in range(0,3):
      c[i] = string.atof( c[i] )
    # end for
    j = string.atoi( c[3] )
    s = c[4]
    self.add_atom( AtomPosition( Atom( s, j ), VectorPosition( [ c[0], c[1], c[2] ] ) ) )
    print ' Transform: insert'
  # end def

  def transform_delete( self, c = [], vmdindex = True  ):
    # 0: no, 1: sym
    no  = string.atoi( c[0] )
    if not vmdindex:
      no -= 1
    # end if
    sym = c[1]
    atom = self.atoms[no]
    if atom.symbol() != sym:
      print ' Warning: symbol mismatch' 
    atom.info()
    self.atoms.remove( atom )
    self.gen_species()
    self.order()
    print ' Transform: delete'
  # end def

  def transform_vcrop( self, c = [], invert = False ):
    for i in range(0,4):
      c[i] = string.atof( c[i] )
    # end for
    r = c[3]
    origo = numpy.array( [ c[0], c[1], c[2] ] )
    d = numpy.zeros( 3 )
    no = c[4]

    convert = False
    if self.position_type == PositionTypes.Direct:
      convert = True
    # end if

    tot = 0
    rem = 0

    removed  = []
    remno    = []
    keepno   = []
    nokeepno = []
    for a in self.atoms:
      if convert:
        pos = self.position_cart( a.position() )
      else:
        pos = a.position()
      # end if
      d   = pos - origo
      dr  = 0.000
      for i in range(0,3):
        dr += d[i]*d[i]
      # end for
      dr = math.sqrt( dr )

      if invert:
        if dr < r:
          # self.atoms.remove( a )
          removed.append( a )
          rem += 1
          remno.append( a.no() )
        else:
          keepno.append( a.no() )
        # end if
      else:
        if dr > r:
          # self.atoms.remove( a )
          removed.append( a )
          rem += 1
          remno.append( a.no() )
        else:
          keepno.append( a.no() )
        # end if
      # end if
      tot += 1
    # end for
    for a in removed:
      self.atoms.remove( a )
    # end for
    for ino in keepno:
      if ino > no:
        nokeepno.append( ino - 1 )
      else:
        nokeepno.append( ino )
    # end for

    print ' Transform: vcrop',tot,rem,tot-rem
    # print remno
    # print keepno
    avpstr = "atomlist = "
    for ino in nokeepno:
      avpstr += " " + str(ino)
    # end for
    print ""
    print "Origo shifted"
    print avpstr

    avpstr = "atomlist = "
    for ino in keepno:
      avpstr += " " + str(ino)
    # end for
    print ""
    print "Normal"
    print avpstr

    print self.lattice_vectors

    self.gen_species()
    self.order()
  # end def


  def transform_icrop( self, c = [], vmdindex = True ):
    self.transform_crop( c, vmdindex, True )
  # end def


  def transform_crop( self, c = [], vmdindex = True, invert = False ):
    no = string.atoi( c[0] )
    r  = string.atof( c[2] )
    if not vmdindex:
      no -= 1
    # end if
    sym = c[1]
    atom = self.atoms[no]
    if atom.symbol() != sym:
      print ' Warning: symbol mismatch' 

    if self.position_type == PositionTypes.Direct:
      origo = self.position_cart( atom.position() )
    else:
      origo = atom.position()

    self.transform_vcrop( [ origo[0], origo[1], origo[2], r, no ], invert )
    print ' Transform: crop',no,sym,origo
  # end def


  def transform_stretch( self, c = [], vmdindex = True ):
    atoms = []

    c[0] = string.atoi( c[0] )
    c[2] = string.atoi( c[2] )
    if not vmdindex:
      c[0] -= 1
      c[2] -= 1
    # end if

    s = string.atof( c[4] )
    atoms.append( self.atoms[c[0]] )
    atoms.append( self.atoms[c[2]] )

    if atoms[0].symbol() != c[1]:
      print ' Warning: symbol mismatch' 
    # end if
    if atoms[1].symbol() != c[3]:
      print ' Warning: symbol mismatch' 
    # end if

    a = atoms[0].position()
    b = atoms[1].position()
    # print a
    # print b
    d = a - b
    dn = 0.000
    for i in range(0,3):
      dn += d[i]*d[i]
    # end if
    dn = math.sqrt( dn )
    du = d / dn
    su = 0.500 * ( 1.000 - s )*du
    # print su
    atoms[0].shift( -su )
    atoms[1].shift(  su )
    print ' Transform: stretch'
  # end def
  
  def transform_scc( self, c = [] ):
    for i in range(0,6):
      c[i] = string.atoi( c[i] )
    # end for
    repeate = numpy.array( c )
    repeate = repeate.reshape(3,2)
    self.cart()
    self.super( repeate )
    self.gen_species()
    self.order()
    print ' Transform: scc'  
  # end def
  
# end class Geometry

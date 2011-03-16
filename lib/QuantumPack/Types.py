#
# Types package
#

import sys
import copy
import string
import numpy

class Enum( object ):
  def __init__( self, elist ):
    for num, name in enumerate( elist.split() ) :
      setattr( self, name, num )
    # end for
  # end def
# end class


PositionTypes = Enum( 'Direct Cart' )
PositionTypesDict = { PositionTypes.Direct : 'Direct', PositionTypes.Cart : 'Cart' }
IOTypes = Enum( 'Input Output' )

def TF( logical ):
  if logical:
    return 'T'
  return 'F'
# end def

class Debug:
  def __init__( self, verbose = False, debug = False ):
    self.verbose = verbose
    self.debug   = debug
  # end def
# end class


class Buffer:
  def __init__( self ):
    self.lc    = 0
    self.line  = ""
    self.lines = {} 
  # end def

  def clean( self ):
    self.lc = 0
    self.lines = {}
  # end def

  def rewind( self ):
    self.lc = 0
  # end def

  def read( self, lines = None ):
    self.clean()
    for line in lines:
      self.lc += 1
      self.lines[self.lc] = line.strip()
    # end for
    self.rewind()
  # end def

  def getline( self ):
    self.lc += 1
    self.line = self.lines[self.lc]
    return self.line
  # end def

  def putline( self, line = None ):
    self.lc += 1
    self.line = line
    self.lines[self.lc] = self.line
  # end def
# end class


class Atom:
  def __init__( self, symbol = "", no = 0, cl_shift = 0.000 ):
    self.symbol = symbol
    # not the atomic number !
    self.no     = no
    self.rno    = no
    self.cl_shift = cl_shift
  # end def
# end class


class VectorPosition:
  def __init__( self, vec = numpy.zeros( 3 ), moveable = None ):
    self.position  = numpy.array( vec )
    self.force     = numpy.zeros( 3 )
    self.velocity  = numpy.zeros( 3 )
    self.moveable  = []
    if( moveable == None ):
      for i in range(0,3):
        self.moveable.append( True )
      # end for
    else:
      for m in moveable:
        if string.upper( m ) == 'T':
          self.moveable.append( True )
        else:
          self.moveable.append( False )
        # end if
      # end for
    # end if
  # end def
# end class


class AtomPosition:
  def __init__( self, atom = None, pos = None ):
    self.atom = atom
    self.pos  = pos
  # end def

  def symbol( self, newsym = None ):
    if newsym != None:
      self.atom.symbol = newsym
    # end if
    return self.atom.symbol
  # end def

  def position( self, newpos = None ):
    if newpos != None:
      self.pos.position = newpos
    # end if
    return self.pos.position
  # end def

  def moveable( self ):
    return self.pos.moveable
  # end def

  def velocity( self ):
    return self.pos.velocity
  # end def

  def no( self ):
    return self.atom.no
  # end def

  def rno( self ):
    return self.atom.rno
  # end def

  def cl_shift( self ):
    return self.atom.cl_shift
  # end def

  def info( self ):
    print " %4d" % self.no(), "%2s" % self.symbol(), self.position(), self.moveable()
  # end def

  def shift( self, S = numpy.zeros( 3 ) ):
    for i in range( 0, 3 ):
      self.pos.position[i] += S[i]
    # end for
  # end def
# end class


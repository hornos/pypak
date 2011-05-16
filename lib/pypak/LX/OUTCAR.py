#
# Types package
#

import sys
import copy
import string

from pypak.Math import *
from pypak.LX.Lexer import Lexer

class LX( Lexer ):
  def __init__( self, path = None, sysopts = { "verbose" : False, "debug" : False } ):
    Lexer.__init__( self, path, sysopts )
    self.tokens.extend( ['INCAR_TAG', 'TAG', 'LABEL',
                         'ITER' ] )
    self.states = [('TF','inclusive')]
    self.hc = 0
    self.c = 0
    self.it = ""
  # end def

  def t_INCAR_TAG( self, t ):
    r'[A-Z0-9_]+\ *=\ *[A-Z0-9._-]+'
    if self.verbose:
      print "INCAR_TAG:" + t.value
    # pass
  # end def

  def t_TAG( self, t ):
    r'[A-Za-z_][a-z_ ]*\ *=\ *[A-Z0-9._-][A-Z0-9._ -]*'
    arr = t.value.split("=")
    key = arr[0].strip()
    val = arr[1].strip()
    #if key == "ions per type":
    #  print val
    # end if
    if self.verbose:
      print "TAG:" + t.value
    # pass
  # end def

  def t_LABEL( self, t ):
    r'[A-Za-z_][a-z_ ]*\ *:\ *[A-Z0-9._-][A-Z0-9._ -]*'
    arr = t.value.split(":")
    key = arr[0].strip()
    val = arr[1].strip()
    if key == "total drift":
      td = L2N( S2F( val ) )
      if td > 0.1:
        print "HIGH Total Drift: " + str( td )
   # end if
    if self.verbose:
      print "LABEL:" + t.value
    # pass
  # end def

  def t_ITER( self, t ):
    r'Iteration\ *[0-9]+\(\ *[0-9]+\)'
    self.it = t.value
  # def

  def t_TF_end( self, t ):
    r'\ *-+$'
    if self.hc == 0:
      self.hc += 1
    else:
      t.lexer.begin('INITIAL')
      self.hc = 0
      self.c
  # end def

  def t_begin_TF( self, t ):
    r'TOTAL-FORCE'
    self.c = 0
    print "\n" + self.it
    t.lexer.begin('TF')
  # end def

  def t_TF_POSVEC( self, t ):
    r'([0-9.-]+\ +)+[0-9.-]+'
    posvec = S2F( t.value )
    tf = L2N( posvec[3:] )
    if tf > 0.1:
      print "%4d." % self.c + " HIGH Force: " + str( tf )
    self.c += 1
  # end def
# end class

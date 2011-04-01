#
# Types package
#

import sys
import copy
import string

from pypak.Macros import *
from pypak.LX.Lexer import Lexer

class LX( Lexer ):
  def __init__( self, path = None, sysopts = { "verbose" : False, "debug" : False } ):
    Lexer.__init__( self, path, sysopts )
    self.tokens.extend( ['INCAR_TAG', 'TAG', 'LABEL' ] )
  # end def

  def t_INCAR_TAG( self, t ):
    r'[A-Z0-9_]+\ *=\ *[A-Z0-9._-]+'
    if self.verbose:
      print "INCAR_TAG:" + t.value
    pass
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
    pass
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
    pass
  # end def
# end class

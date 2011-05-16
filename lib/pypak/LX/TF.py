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

    self.tokens.extend( [ 'TF_KEYWORD',
                          'TF_DATA',
                          'TF_COMMENT' ] )
    self.keyword = ''
    self.content = []
    self.geom    = None
    self.result  = None

  # end def

  # complex rules
  def t_TF_COMMENT( self, t ):
    r'\#.*'
    pass
  # end def

  def t_TF_KEYWORD( self, t ):
    r'@[a-zA-Z_]+'
    t.value = str(t.value)
    t.value = t.value.strip('@')
    self.keyword = t.value
    self.content = []
    return t
  # end def


  def t_TF_DATA( self, t ):
    r'[0-9a-zA-Z. -<>]+'
    self.content = t.value.split()
    method = 'TF_' + self.keyword
    self.result = getattr( self.geom, method )( self.content )
    return t
  # end def

# end class

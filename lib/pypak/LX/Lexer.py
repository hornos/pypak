#
# Types package
#

import sys
import copy
import numpy
import ply.lex as lex

from pypak.Types    import *

class Lexer( Debug ):

  def __init__( self, path = None, sysopts = { "verbose" : False, "debug" : False } ):
    Debug.__init__( self, sysopts )
    self.path   = path
    self.lexer  = None
    self.t_ignore = r' '
    self.tokens = ['COMMENT']
  # end def

  def t_COMMENT( self, t ):
    r'\#.*'
    if self.verbose:
      print t.value
    pass
  # end def

  def t_newline( self, t ):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
  # end def


  def t_error( self, t ):
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
  # end def

  # constructor
  def build( self, **kwargs ):
    self.lexer = lex.lex( object = self, **kwargs )
  # end def

  def tokenize( self, data ):
    self.lexer.input( data )
    while True:
      tok = self.lexer.token()
      if not tok: break
      # print tok,self.content
    # end while
  # end def

  def process( self ):
    inp = open( self.path, "r" )
    for line in inp:
      self.tokenize( line )
    # end for
    inp.close()
  # end def

# end class

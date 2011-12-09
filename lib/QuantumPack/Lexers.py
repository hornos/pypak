#
# Types package
#

import sys
import copy
import numpy
import ply.lex as lex

class Transform:
  keyword = ''
  content = []
  geom    = None

  # token list
  tokens = ( 'TRANSFORM_KEYWORD', 'TRANSFORM_TRANSFORM_LINE',
             'TRANSFORM_COMMENT' )

  # simple rules

  # complex rules
  def t_TRANSFORM_COMMENT( self, t ):
    r'\#.*'
    pass
  # end def

  def t_TRANSFORM_KEYWORD( self, t ):
    r'@[a-zA-Z_]+'
    t.value = str(t.value)
    t.value = t.value.strip('@')
    self.keyword = t.value
    self.content = []
    return t
  # end def


  def t_TRANSFORM_TRANSFORM_LINE( self, t ):
    r'[0-9-]+[0-9a-zA-Z. -<>]*'
    self.content = t.value.split()
    if self.keyword == 'shift':
      self.geom.transform_shift( self.content )
    if self.keyword == 'vshift':
      self.geom.transform_vshift( self.content )
    if self.keyword == 'lshift':
      self.geom.transform_lshift( self.content )
    if self.keyword == 'rshift':
      self.geom.transform_rshift( self.content )
    if self.keyword == 'cshift':
      self.geom.transform_cshift( self.content )
    if self.keyword == 'center':
      self.geom.transform_center( self.content )
    if self.keyword == 'stretch':
      self.geom.transform_stretch( self.content )
    if self.keyword == 'insert':
      self.geom.transform_insert( self.content )
    if self.keyword == 'crop':
      self.geom.transform_crop( self.content )
    if self.keyword == 'icrop':
      self.geom.transform_icrop( self.content )
    if self.keyword == 'vcrop':
      self.geom.transform_vcrop( self.content )
    if self.keyword == 'scc':
      self.geom.transform_scc( self.content )
    if self.keyword == 'latrot':
      self.geom.transform_latrot( self.content )
    if self.keyword == 'mirror':
      self.geom.transform_mirror( self.content )
    if self.keyword == 'rot':
      self.geom.transform_rot( self.content )
    return t
  # end def


  def t_newline( self, t ):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
  # end def


  # ignore white spaces
  # TODO: do it better for tabs
  t_ignore = r' '


  def t_error( self, t ):
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
  # end def


  # constructor
  def build( self, **kwargs ):
    self.lexer = lex.lex( module = self, **kwargs )
  # end def


  def tokenize( self, data ):
    self.lexer.input( data )
    while True:
      tok = self.lexer.token()
      if not tok: break
      # print tok,self.content
    # end while
  # end def

  def process( self, filename = "", geom = None ):
    inp = open( filename, "r" )
    self.geom = geom

    for line in inp:
      self.tokenize( line )
    # end for

    inp.close()
  # end def

# end class

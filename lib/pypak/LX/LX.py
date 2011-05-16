#
# IO Package
# TAB: 4
#
import os
import sys
import string
from pypak.Types import *

# try to load io handler based on type
class LX( Debug ):
  def __init__( self, path = None, type = None, sysopts = { "verbose" : False, "debug" : False } ):
    Debug.__init__( self, sysopts )

    # try to load handler
    hm = 'pypak.LX.' + str( type )
    m = __import__( hm, globals(), locals(), -1 )
    self.handler = m.LX( path, sysopts )
  # end def __init__

  def process( self ):
    self.handler.process()
  # end def

  def build( self ):
    self.handler.build()
  # end def

  def read( self ):
    self.build()
    self.process()
    return self.result()
  # end def

  def geom( self, geom = None ):
    if geom == None:
      return self.handler.geom
    else:
      self.handler.geom = geom
  # end def

  def result( self ):
    return self.handler.result
  # end def
# end class

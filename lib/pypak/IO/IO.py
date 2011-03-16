#
# IO Package
# TAB: 4
#
import os
import sys
import string
import numpy
from pypak.Types import *

# try to load io handler based on type
class IO( Debug ):
  def __init__( self, path = None, type = None, opts = "rw", sysopts = { "verbose" : False, "debug" : False } ):
    Debug.__init__( self, sysopts )

    if string.find( opts, "r" ) > -1:
      if not os.path.isfile( path ) :
        raise IOError, str( path )
      # end if
    # end if
    # try to load handler
    handler_module = 'pypak.IO.' + str( type )
    module = __import__( handler_module, globals(), locals(), -1 )
    self.handler = module.IO( path, opts, sysopts )
  # end def __init__

  def open( self ):
    self.handler.open()
  # end def

  def close( self ):
    self.handler.close()
  # end def

  def read( self, opts = None ):
    self.handler.read( opts )
  # end def

  def write( self, opts = None ):
    self.handler.write( opts )
  # end def

  def geom( self, geom = None ):
    if geom != None:
      self.handler.geom = geom
    # end if
    return self.handler.geom
  # end def

  def command( self, cmd = None, argv = None ):
    cmdfn = getattr( self.handler, cmd )
    return cmdfn( argv )
  # end def
# end class

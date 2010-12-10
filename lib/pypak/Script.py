#
# Script
#

import os
import string
import ConfigParser
from optparse import OptionParser
import numpy
from pypak.Types import *

class Script( Debug ):
  def __init__( self, scn = os.path.basename( sys.argv[0] ), 
                      gpc = os.path.dirname( sys.argv[0] ) + "/pypak.ini" ):
    Debug.__init__( self )
    self.scn    = scn
    self.optpar = OptionParser()
    self.gpc    = gpc
    self.upc    = None
    self.gpcpar = ConfigParser.ConfigParser()
    self.upcpar = ConfigParser.ConfigParser()
  # end def

  def opt( self, *args, **kwargs ):
    self.optpar.add_option( *args, **kwargs )
  # end def

  def par( self ):
    return self.optpar.parse_args()
  # end def

  def ini( self ):
    self.opt( "-c", "--config", action = "store", type = "string", dest = "upc", 
              default = "config.ini", help = "User Configuration File (default: config.ini)" )

    self.opt( "-v", "--verbose", action = "store_true", dest = "verbose", 
              default = False, help = "Verbose Mode" )

    self.opt( "-w", "--debug", action = "store_true", dest = "debug", 
              default = False, help = "Debug Mode" )


    (opts, args) = self.par()
    self.verbose = opts.verbose
    self.debug   = opts.debug
    self.upc     = opts.upc

    ## Global Config
    try:
      self.gpcpar.readfp( open( self.gpc ) )
      if self.verbose :
        print ' Global: ' + self.gpc
    except:
      if self.verbose :
        print ' Missing: ' + self.gpc
    # end try

    ## Read User Config
    try:
      self.upcpar.readfp( open( self.upc ) )
      if self.verbose :
        print ' User: ' + self.upc
    except:
      if self.verbose :
        print ' Missing: ' + self.upc
    # end try
  # end def


  def cfg( self, item = None ):
    try:
      return self.upcpar.get( self.scn, item )
    except:
      try:
        return self.gpcpar.get( self.scn, item )
      except:
        raise
      # end try
    # end try
  # end def


  def cfgi( self, item = None ):
    return string.atoi( self.cfg( item ) )
  # end def


  def cfgf( self, item = None ):
    return string.atof( self.cfg( item ) )
  # end def


  def cfgarr( self, item = None ):
    line = self.cfg( item )
    return line.split();
  # end def


  def cfgarri( self, item = None ):
    arr = self.cfgarr( item )
    for i in range( 0, len( arr ) ):
      arr[i] = string.atoi( arr[i] )
    # end for
    return numpy.array( arr )
  # end def


  def cfgarrf( self, item = None ):
    arr = self.cfgarr( item )
    for i in range( 0, len( arr ) ):
      arr[i] = string.atof( arr[i] )
    # end for
    return numpy.array( arr )
  # end def
# end class

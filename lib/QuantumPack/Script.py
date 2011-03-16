#
# Script
#

import string
import ConfigParser
from optparse import OptionParser
import numpy
from QuantumPack.Types import *

class Script( Debug ):
  def __init__( self, script_name = 'QuantumPack Script', quantumpack_home = None, quantumpack_config = None ):
    Debug.__init__( self )
    self.script_name = script_name
    self.opt_parser  = OptionParser()
    self.quantumpack_home     = quantumpack_home
    self.quantumpack_config   = quantumpack_config
    self.global_config_parser = ConfigParser.ConfigParser()
    self.user_config_parser   = ConfigParser.ConfigParser()
  # end def


  def option( self, sopt, lopt, action, type, dest, default, help ):
    self.opt_parser.add_option( sopt, lopt, action = action, type = type, dest = dest, 
                                default = default, help = help )
  # end def

  def parse( self ):
    return self.opt_parser.parse_args()
  # end def


  def init( self ):

    self.opt_parser.add_option( "-c", "--config",
                        action = "store", type = "string",
                        dest = "user_config", default = "config.ini",
                        help = "User Configuration File (default: config.ini)" )

    self.opt_parser.add_option( "-v", "--verbose",
                        action = "store_true",
                        dest = "verbose", default = False,
                        help = "Verbose" )

    self.opt_parser.add_option( "-w", "--debug",
                        action = "store_true",
                        dest = "debug", default = False,
                        help = "Debug verbose" )


    (options, args) = self.opt_parser.parse_args()
    self.verbose = options.verbose
    self.debug   = options.debug
    ## Configs
    global_config = self.quantumpack_home + '/' + self.quantumpack_config
    user_config   = options.user_config
    ## Read Global Config
    try:
      self.global_config_parser.read( global_config )
      if self.debug and self.verbose :
        print ' Reading: ' + global_config
    except:
      if self.debug and self.verbose :
        print ' Warning: no global config ' + global_config
    # end try
    ## Read User Config
    try:
      self.user_config_parser.read( user_config )
      if self.debug and self.verbose :
        print ' Reading: ' + user_config
    except:
      if self.debug and self.verbose :
        print ' Warning: no user config ' + user_config
    # end try
  # end def


  def main( self ):
    if self.debug :
      print "Main Function"
    # end if
  # end def


  def getopt( self, item = None ):
    try:
      return self.user_config_parser.get( self.script_name, item )
    except:
      try:
        return self.global_config_parser.get( self.script_name, item )
      except:
        raise
      # end try
    # end try
  # end def


  def getopti( self, item = None ):
    return string.atoi( self.getopt( item ) )
  # end def


  def getoptf( self, item = None ):
    return string.atof( self.getopt( item ) )
  # end def


  def getoptarr( self, item = None ):
    line = self.getopt( item )
    return line.split();
  # end def


  def getoptarri( self, item = None ):
    arr = self.getoptarr( item )
    for i in range( 0, len( arr ) ):
      arr[i] = string.atoi( arr[i] )
    # end for
    return numpy.array( arr )
  # end def


  def getoptarrf( self, item = None ):
    arr = self.getoptarr( item )
    for i in range( 0, len( arr ) ):
      arr[i] = string.atof( arr[i] )
    # end for
    return numpy.array( arr )
  # end def
# end class

#!/usr/bin/env python
#TAB: 8
import os
import sys
import string

### BEGIN HEADER
script_name = os.path.basename( sys.argv[0] )
sys.path.append( os.path.dirname( sys.argv[0] ) + "/../lib" )
quantumpack_home   = os.path.dirname( sys.argv[0] ) + "/.."
quantumpack_config = "qppak.ini"
### END HEADER

###
### BEGIN PROGRAM CLASS
###
from QuantumPack.Script import Script
from QuantumPack.FileIO.FileIO import FileIO

class Program( Script ):
  def __init__( self, script_name, quantumpack_home, quantumpack_config ):
    Script.__init__( self, script_name, quantumpack_home, quantumpack_config )

    self.opt_parser.add_option( "-i", "--input",
                         action = "store", type = "string",
                         dest = "input_file", default = "input.UEIG",
                         help = "Input", 
                         metavar="INPUT" )
    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.opt_parser.parse_args()
    try:
      sigma = self.getoptf( 'sigma' )
    except:
      sigma = 0.100
    # end try

    try:
      alpha = self.getoptf( 'alpha' )
    except:
      alpha = 2.000
    # end try

    try:
      kpt = self.getoptf( 'kpt' )
    except:
      kpt = 1
    # end try

    try:
      channels = self.getopti( 'channels' )
    except:
      channels = 2048
    # end try


    sysopts = { "verbose" : self.verbose, "debug" : self.debug }
    input_file = options.input_file
    try:
      input_ueig = FileIO( input_file, 'UEIG', "r", sysopts )
    except:
      if self.debug:
        raise
      print ' Error: ' + input_file
      return 0
    # end try
    input_ueig.read()
    # print input_ueig.handler.ibuffer.lines

    avg_cl_shift = input_ueig.command( 'gendos', { 'sigma' : sigma, 
                                                   'alpha' : alpha, 
                                                   'kpt' : kpt,
                                                   'channels' : channels} )

  # end def main
###
### END PROGRAM CLASS
###


###
### BEGIN MAIN
###
if __name__ == '__main__':
  program = Program( script_name, quantumpack_home, quantumpack_config )
  program.main()
# end if
###
### END MAIN
###

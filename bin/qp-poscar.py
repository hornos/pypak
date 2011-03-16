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


### BEGIN PROGRAM CLASS
from QuantumPack.Script        import Script
from QuantumPack.FileIO.FileIO import FileIO
from QuantumPack.Types         import *
from QuantumPack.Geometry      import Geometry


class Program( Script ):
  def __init__( self, script_name, quantumpack_home, quantumpack_config ):
    Script.__init__( self, script_name, quantumpack_home, quantumpack_config )

    self.opt_parser.add_option( "-i", "--input",
                         action = "store", type = "string",
                         dest = "input_name", default = "input.POSCAR",
                         help = "Input" )

    self.opt_parser.add_option( "-o", "--output",
                         action = "store", type = "string",
                         dest = "output_name", default = "output.cart.POSCAR",
                         help = "Output" )

    self.opt_parser.add_option( "-d", "--direct",
                        action = "store_true",
                        dest = "direct", default = False,
                        help = "Direct" )

    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.opt_parser.parse_args()
    input_name  = options.input_name
    output_name = options.output_name
    direct = options.direct

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    try:
      input_file  = FileIO( input_name,'POSCAR', "r", sysopts )
    except Exception as ex:
      print 'Error: ' + str( ex )
    # end try

    input_file.read()
    geom = input_file.geom()
    # geom.check()

    position_type = PositionTypes.Cart
    if direct:
      position_type = PositionTypes.Direct
    # end if

    try:
      output_file = FileIO( output_name,'POSCAR', "w+", sysopts )
      output_file.geom( geom )
      output_file.write( { 'position_type' : position_type } )
    except Exception as ex:
      print 'Error: ' + str( ex )
    # end try
  # end def
# end class


### BEGIN MAIN
if __name__ == '__main__':
  program = Program( script_name, quantumpack_home, quantumpack_config )
  program.main()
### END MAIN

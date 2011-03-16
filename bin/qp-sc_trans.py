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
from QuantumPack.Lexers        import Transform
from QuantumPack.Geometry      import Geometry


class Program( Script ):
  def __init__( self, script_name, quantumpack_home, quantumpack_config ):
    Script.__init__( self, script_name, quantumpack_home, quantumpack_config )

    self.opt_parser.add_option( "-i", "--input",
                         action = "store", type = "string",
                         dest = "input_name", default = "",
                         help = "Input" )

    self.opt_parser.add_option( "-t", "--transform",
                         action = "store", type = "string",
                         dest = "trans_name", default = "input.tf",
                         help = "Transform" )

    self.opt_parser.add_option( "-o", "--output",
                         action = "store", type = "string",
                         dest = "output_name", default = "transform",
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
    trans_name  = options.trans_name
    direct = options.direct
    
    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    # position type
    position_type = PositionTypes.Cart
    if direct:
      position_type = PositionTypes.Direct
    # end if

    # read inputs
    try:
      input_file = FileIO( input_name, 'POSCAR', "r", sysopts )
    except Exception as ex:
      print ' Error: ' + str( ex )
      return 0
    # end try
    input_file.read()
    geom = input_file.geom()

    try:
      trans = Transform()
      trans.build()
      trans.process( trans_name, geom )
    except Exception as ex:
      print ' No transformation: ' + str( ex )
      if self.verbose:
        raise
    # end try
    
    geom.gen_species()
    geom.order()
    write_geom( output_name, sysopts, geom, position_type )

  # end def main

### END PROGRAM CLASS

def write_geom( name = "output", sysopts = { "verbose" : False, "debug" : False }, geom = None, position_type = PositionTypes.Cart ):
    output = FileIO( name + ".xyz",'xyz', "w+", sysopts )
    output.geom( geom )
    output.write()

    output = FileIO( name + ".POSCAR",'POSCAR', "w+", sysopts )
    output.geom( geom )
    output.write( { "position_type" : position_type } )
# end def


### BEGIN MAIN
if __name__ == '__main__':
  program = Program( script_name, quantumpack_home, quantumpack_config )
  program.main()
### END MAIN

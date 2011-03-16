#!/usr/bin/env python
#TAB: 8
import os
import sys
import string

### BEGIN HEADER
sys.path.append( os.path.dirname( sys.argv[0] ) + "/../lib" )
quantumpack_home   = os.path.dirname( sys.argv[0] ) + "/.."
quantumpack_config = "qppak.ini"
### END HEADER


### BEGIN PROGRAM CLASS
from QuantumPack.Script import Script
from QuantumPack.FileIO.FileIO import FileIO
from QuantumPack.Types import *


class Program( Script ):
  def __init__( self, script_name, quantumpack_home, quantumpack_config ):
    Script.__init__( self, script_name, quantumpack_home, quantumpack_config )

    self.opt_parser.add_option( "-i", "--input",
                         action = "store", type = "string",
                         dest = "input_desc", default = "POSCAR",
                         help = "Input", 
                         metavar="INPUT" )

    self.opt_parser.add_option( "-e", "--embed",
                         action = "store", type = "string",
                         dest = "embed_desc", default = "POSCAR",
                         help = "Embed", 
                         metavar="EMBED" )

    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.opt_parser.parse_args()

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }
    input_desc = options.input_desc
    (input_file,input_sym,input_no) = input_desc.split( ":" )
    input_no = string.atoi( input_no )

    embed_desc = options.embed_desc
    (embed_file,embed_sym,embed_no) = embed_desc.split( ":" )
    embed_no = string.atoi( embed_no )

    try:
      input_poscar = FileIO( input_file, 'POSCAR', "r", sysopts )
      embed_poscar = FileIO( embed_file, 'POSCAR', "r", sysopts )
    except Exception as ex:
      print ' Error: ' + str( ex )
      return 0
    # end try
    input_poscar.read()
    embed_poscar.read()
    
    geom = input_poscar.geom()
    geom.embed( embed_poscar.geom(), embed_sym, embed_no, input_sym, input_no )
    
    geom.gen_species()
    geom.order()
    
    write_geom( 'embed', sysopts, geom )
    
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

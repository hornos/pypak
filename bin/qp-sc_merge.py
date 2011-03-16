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
                         dest = "input_files", default = "",
                         help = "Input" )

    self.opt_parser.add_option( "-t", "--transform",
                         action = "store", type = "string",
                         dest = "trans_name", default = "merge.tf",
                         help = "Transform" )

    self.opt_parser.add_option( "-o", "--output",
                         action = "store", type = "string",
                         dest = "output_name", default = "merge",
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
    input_files_arr = {}
    input_arr = {}
    input_files = options.input_files
    output_name = options.output_name
    trans_name  = options.trans_name
    direct = options.direct
    
    merge_geom = Geometry( 'Merge' )
    merge_geom.position_type = PositionTypes.Cart

    try:
      for inp in input_files.split( "," ):
        ( sym, input_file ) = inp.split( ":" )
        input_files_arr[sym] = input_file
      # end for
    except Exception as ex:
      print ' Error: ' + str( ex )
      return 0
    # end try

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }
    # read inputs
    for inp in input_files_arr:
      sym = inp
      input_file = input_files_arr[inp]
      try:
        input_arr[sym] = FileIO( input_file, 'SCCOUT', "r", sysopts )
      except Exception as ex:
        print ' Error: ' + str( ex )
        return 0
      # end try
      input_arr[sym].handler.set( 'global_specie', sym )
      input_arr[sym].read()

      geom = input_arr[sym].geom()
      geom.name = input_file
      # geom.check()
      try:
        verbose = merge_geom.merge( geom, True, False )
        if self.verbose:
          print verbose
      except Exception as ex:
        print ' Error: ' + str( ex )
        return 0
      # end try
    # end for


    position_type = PositionTypes.Cart
    if direct:
      position_type = PositionTypes.Direct
    # end if

    # # merge check
    # merge_geom.wignercell()
    # # write out check geoms
    merge_geom.order()
    write_geom( output_name, sysopts, merge_geom, position_type )

    try:
      trans = Transform()
      trans.build()
      trans.process( trans_name, merge_geom )
    except Exception as ex:
      print str( ex )
      #if self.verbose:
        # raise
    # end try

    write_geom( output_name + ".transform", sysopts, merge_geom, position_type )

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

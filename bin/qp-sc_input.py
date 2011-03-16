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
from QuantumPack.Script import Script
from QuantumPack.FileIO.FileIO import FileIO
from QuantumPack.Types import *


class Program( Script ):
  def __init__( self, script_name, quantumpack_home, quantumpack_config ):
    Script.__init__( self, script_name, quantumpack_home, quantumpack_config )

    self.opt_parser.add_option( "-i", "--input",
                         action = "store", type = "string",
                         dest = "input_file", default = "POSCAR",
                         help = "Input", 
                         metavar="INPUT" )
    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.opt_parser.parse_args()
    try:
      scale = self.getoptarri( 'scale' )
    except:
      print ' Error: no scale'
      return 0
    # end try

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }
    input_file = options.input_file
    try:
      input_poscar = FileIO( input_file, 'POSCAR', "r", sysopts )
    except Exception as ex:
      print ' Error: ' + str( ex )
      return 0
    # end try
    input_poscar.read()

    geom = input_poscar.geom()
    
    for s in geom.species:
      output_file = str( s ) + "-" + input_file + ".SCCIN"
      # print output_file
      try:
        output_in = open( output_file, "w+" )
      except Exception as ex:
        print ' Error: ' + str( ex )
        return 0
      # end try

      output_in.write( "transformation\n" )
      output_in.write( "%9.6f %9.6f %9.6f\n" % (scale[0], 0.000000, 0.000000) )
      output_in.write( "%9.6f %9.6f %9.6f\n" % (0.000000, scale[1], 0.000000) )
      output_in.write( "%9.6f %9.6f %9.6f\n" % (0.000000, 0.000000, scale[2]) )
      output_in.write( "userdef\n" )
      
      for lv in geom.lattice_vectors:
        output_in.write( "%20.16f %20.16f %20.16f\n" % (lv[0], lv[1], lv[2]) )
      # end for
      
      output_in.write( "%d\n" % geom.species[s] )
      # find specie s
      for atom in geom.atoms:
        if atom.symbol() == s:
          pos = geom.position( atom, PositionTypes.Cart )
          output_in.write( "%20.16f %20.16f %20.16f\n" % (pos[0], pos[1], pos[2]) )
        # end if
      # end for
      output_in.write( "\n0.000 0.000 0.000\n" )
      output_in.close()

    # end for s

    # check geom
    output_file = "primitive.xyz"
    try:
      output_xyz = open( output_file, "w+" )
    except Exception as ex:
      print ' Error: ' + str( ex )
      return 0
    # end try
    output_xyz.write( "%d\n\n" % geom.number_of_atoms() )
    for s in geom.species:
      for atom in geom.atoms:
        if atom.symbol() == s:
          pos = geom.position( atom, PositionTypes.Cart )
          output_xyz.write( "%2s %20.16f %20.16f %20.16f\n" % (s, pos[0], pos[1], pos[2]) )
        # end if
      # end for
    # end for
    output_xyz.close()
  # end def main

### END PROGRAM CLASS


### BEGIN MAIN
if __name__ == '__main__':
  program = Program( script_name, quantumpack_home, quantumpack_config )
  program.main()
### END MAIN

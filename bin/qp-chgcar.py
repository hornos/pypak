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
  def __init__( self, sc_name, qp_home, qp_config ):
    Script.__init__( self, sc_name, qp_home, qp_config )
    # d = a * m + b * s
    # option:    short  long      action   type      destination  default  help
    self.option( "-m",  "--min",  "store", "string", "min_name",  "min",   "Minuend" )
    self.option( "-a",  "--amin", "store", "string", "amin",      "1.000", "Minuend Coeff" )
    self.option( "-s",  "--sub",  "store", "string", "sub_name",  "sub",   "Subtrahend" )
    self.option( "-b",  "--bsub", "store", "string", "bsub",      "-1.000","Subtrahend Coeff" )
    self.option( "-d",  "--diff", "store", "string", "dif_name",  "diff",  "Difference" )
    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()
    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    a = string.atof(opts.amin)
    b = string.atof(opts.bsub)

    # read inputs
    min_file = FileIO( opts.min_name, 'CHGCAR', "r", sysopts )
    min_file.read()

    sub_file = FileIO( opts.sub_name, 'CHGCAR', "r", sysopts )
    sub_file.read()

    min_file.command('add', { 's': sub_file, 'a' : a, 'b' : b} )
    min_file.handler.path = 'diff.CHGCAR'
    min_file.handler.opts = 'w+'
    min_file.handler.buffer = min_file.handler.obuffer
    min_file.write( { 'diff' : True } )
#    write_geom( output_name, sysopts, geom, position_type )

  # end def main

### END PROGRAM CLASS


### BEGIN MAIN
if __name__ == '__main__':
  program = Program( sc_name, qp_home, qp_config )
  program.main()
### END MAIN

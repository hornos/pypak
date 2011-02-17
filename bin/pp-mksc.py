#!/usr/bin/env python
#TAB: 8
import os
import sys
import string

import numpy

### BEGIN HEADER
sys.path.append( os.path.dirname( sys.argv[0] ) + "/../lib" )
### END HEADER

from pypak.Script import Script
from pypak.FileIO.FileIO import FileIO as FIO
from pypak.Lattice import Lattice

class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.opt( "-i", "--input",
              action = "store", type = "string",
              dest = "input_name", default = "POSCAR",
              help = "Input" )

    self.ini()
  # end def __init__

  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.par()

    try:
      scm = self.cfgarri( 'scm' )
    except:
      print ' Error: no scm matrix'
      return 0
    # end try


    sysopts = { "verbose" : self.verbose, "debug" : self.debug }
    input_file = options.input_name
    input_pos = FIO( input_file, 'POSCAR', "r", sysopts )
    input_pos.read()

    sc_geom = Lattice.mksc( geom, scm )

  # end def main
### END PROGRAM CLASS

### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
# end if
### END MAIN


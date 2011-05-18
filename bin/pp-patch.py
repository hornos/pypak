#!/usr/bin/env python
#TAB: 8
import os
import sys
import string

### BEGIN HEADER
sys.path.append( os.path.dirname( sys.argv[0] ) + "/../lib" )
### END HEADER

### BEGIN PROGRAM CLASS
from pypak.Script        import Script
from pypak.IO.IO         import IO
from pypak.Types         import *


class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.opt( "-i", "--input",
              action = "store", type = "string",
              dest = "input_name", default = "POSCAR",
              help = "Input" )

    self.opt( "-d", "--diff",
              action = "store", type = "string",
              dest = "diff_name", default = "diff.POSCAR",
              help = "Reference" )

    self.opt( "-o", "--output",
              action = "store", type = "string",
              dest = "output_name", default = "patch.POSCAR",
              help = "Output" )

    self.ini()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.par()
    input_name  = options.input_name
    output_name = options.output_name
    diff_name   = options.diff_name

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    # read input geometry
    input_file = IO( input_name, 'POSCAR', 'r', sysopts )
    input_file.read()

    diff_file = IO( diff_name, 'diff', 'r', sysopts )
    diff_file.read()

    geom  = input_file.geom()
    dgeom = diff_file.geom()
    pgeom = geom.patch( dgeom )

    # output
    opts = { 'pt' : PT.Cart }
    output_file = IO( output_name, 'POSCAR', "w+", sysopts )
    output_file.geom( pgeom )
    output_file.write( opts )

  # end def
# end class


### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN

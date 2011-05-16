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
from pypak.LX.LX         import LX
from pypak.IO.IO         import IO
from pypak.Types         import *


class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.opt( "-i", "--input",
              action = "store", type = "string",
              dest = "input_name", default = "POSCAR",
              help = "Input" )

    self.opt( "-t", "--trans",
              action = "store", type = "string",
              dest = "trans_name", default = "trans",
              help = "Transform" )

    self.opt( "-o", "--output",
              action = "store", type = "string",
              dest = "output_name", default = "trans.POSCAR",
              help = "Output" )


    self.ini()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.par()
    input_name  = options.input_name
    trans_name  = options.trans_name
    output_name = options.output_name

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    # read input geometry
    input_file = IO( input_name, 'POSCAR', 'r', sysopts )
    input_file.read()

    # transform
    trans_file = LX( trans_name, 'TF', sysopts )
    trans_file.geom( input_file.geom() )
    geom = trans_file.read()

    # output
    opts = { 'pt' : PT.Cart }
    output_file = IO( output_name, 'POSCAR', "w+", sysopts )
    output_file.geom( geom )
    output_file.write( opts )

  # end def
# end class


### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN

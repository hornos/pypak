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
from pypak.Geometry      import Geometry


class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.opt( "-i", "--input",
              action = "store", type = "string",
              dest = "input_name", default = "input.POSCAR",
              help = "Input" )

    self.opt( "-o", "--output",
              action = "store", type = "string",
              dest = "output_name", default = "output",
              help = "Output" )

    self.opt( "-d", "--direct",
              action = "store_true",
              dest = "direct", default = False,
              help = "Direct" )

    self.opt( "-x", "--xyz",
              action = "store_true",
              dest = "xyz", default = False,
              help = "XYZ" )

    self.ini()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.par()
    input_name  = options.input_name
    output_name = options.output_name
    pt = PT.Cart
    if options.direct:
      pt = PT.Direct
    # end if
    output_name += "."+PTD[pt]

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    input_file  = IO( input_name,'POSCAR', "r", sysopts )
    input_file.read()
    geom = input_file.geom()

    fileio = 'POSCAR'
    opts = { 'pt' : pt }
    if options.xyz:
      output_name += '.xyz'
      fileio = 'xyz'
      opts = { 'pt' : PT.Cart }
    else:
      output_name += '.POSCAR'
    # end if
    output_file = IO( output_name,fileio, "w+", sysopts )
    output_file.geom( geom )
    output_file.write( opts )
  # end def
# end class

### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN

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

    self.opt( "-r", "--reference",
              action = "store", type = "string",
              dest = "ref_name", default = "ref.POSCAR",
              help = "Reference" )

    self.opt( "-o", "--output",
              action = "store", type = "string",
              dest = "output_name", default = "diff.POSCAR",
              help = "Output" )

    self.opt( "-l", "--lower",
              action = "store", type = "float",
              dest = "ll", default = 0.1,
              help = "Lower limit" )

    self.opt( "-u", "--upper",
              action = "store", type = "float",
              dest = "ul", default = 1.5,
              help = "Upper limit" )

    self.opt( "-n", "--newno",
              action = "store_true",
              dest = "newno", default = False,
              help = "Atom numbers form the new geometry" )

    self.ini()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.par()
    input_name  = options.input_name
    output_name = options.output_name
    ref_name    = options.ref_name
    ul = options.ul
    ll = options.ll

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    # read input geometry
    input_file = IO( input_name, 'POSCAR', 'r', sysopts )
    input_file.read()

    ref_file = IO( ref_name, 'POSCAR', 'r', sysopts )
    ref_file.read()

    # geom check
    igeom = input_file.geom()
    rgeom = ref_file.geom()

    print "Reference: " + ref_name + "  New: " + input_name
    dgeom = rgeom.diff( igeom, ll, ul, options.newno )

    # output
    opts = { 'pt' : PT.Cart }
    output_file = IO( output_name, 'diff', "w+", sysopts )
    output_file.geom( dgeom )
    output_file.write( opts )

  # end def
# end class


### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN

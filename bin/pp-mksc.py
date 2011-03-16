#!/usr/bin/env python
#TAB: 8
import os
import sys
import string

import numpy

### BEGIN HEADER
sys.path.append( os.path.dirname( sys.argv[0] ) + "/../lib" )
### END HEADER

from pypak.Script  import Script
from pypak.IO.IO   import IO

class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.opt( "-i", "--input",
              action = "store", type = "string",
              dest = "input_name", default = "input.UPOT",
              help = "Input" )

    self.ini()
  # end def __init__

  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.par()

    try:
      msc = self.cfgarri( 'msc' )
      msc = msc.reshape([3,3])
    except:
      print ' Error: no supercell matrix'
      return 0
    # end try

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }
    input_file = options.input_name
    input_pos = IO( input_file, 'POSCAR', "r", sysopts )
    input_pos.read()

    super_geom = input_pos.geom().supercell( msc )

  # end def main
###
### END PROGRAM CLASS
###


###
### BEGIN MAIN
###
if __name__ == '__main__':
  p = Program()
  p.main()
# end if
###
### END MAIN
###

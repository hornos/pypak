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

    self.opt( "-s", "--select",
              action = "store", type = "string",
              dest = "select", default = "0",
              help = "Output" )

    self.ini()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.par()
    input_name  = options.input_name
    select = int(options.select)

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    input_file  = IO( input_name,'POSCAR', "r", sysopts )
    input_file.read()
    geom = input_file.geom()
    atom = geom.get(select)
    atom.info()

    if geom.pt == PT.Cart:
      print "Direct : ", geom.position( atom, PT.Direct )
    else:
      print "Cart : ", geom.position( atom, PT.Cart )
    # end if

  # end def
# end class


### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN

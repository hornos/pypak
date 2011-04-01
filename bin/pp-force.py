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
from pypak.LX.Lexer      import Lexer
from pypak.Types         import *


class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.opt( "-i", "--input",
              action = "store", type = "string",
              dest = "input_name", default = "OUTCAR",
              help = "Input" )

    self.ini()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.par()
    input_name  = options.input_name

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    input_file  = LX( input_name,'OUTCAR', sysopts )
    input_file.build()
    input_file.process()
  # end def
# end class


### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN

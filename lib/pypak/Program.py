#
# Program
#

import os
from pypak.Script import *

class Program( Script ):

  def __init__( self, scn = "pypak program", gpc = os.path.dirname( sys.argv[0] )+"/pypak.ini" ):
    Script.__init__( self, scn, gpc )
    self.opt( "-i", "--input", action = "store", type = "string",
              dest = "input_file", default = "input.dat",
              help = "Input", metavar="INPUT" )
    self.ini()
  # end def

# end class

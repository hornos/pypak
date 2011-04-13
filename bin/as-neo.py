#!/usr/bin/env python
#TAB: 8
import os
import sys
import string

import socket
import time
import re

### BEGIN HEADER
sys.path.append( os.path.dirname( sys.argv[0] ) + "/../lib" )
### END HEADER

### BEGIN PROGRAM CLASS
from state.R466286 import *
from state.R466298 import *
from pypak.Script  import Script


class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.opt( "-i", "--input",
              action = "store", type = "string",
              dest = "input_name", default = "input.txt",
              help = "Input" )

    self.opt( "-u", "--unknown",
              action = "store_true",
              dest = "unknown", default = False,
              help = "Show unknown" )

    self.opt( "-f", "--fast",
              action = "store_true",
              dest = "fast", default = False,
              help = "Fast" )

    self.ini()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.par()
    input_name  = options.input_name
    # open input
    try:
      inp = open( input_name, "r" )
    except:
      sys.exit(1)
    # open db


    for line in inp.readlines():
      line = string.strip( line )
      try:
        cidr.match( line )
      except:
        continue
      # end try
      if re.match("^([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,3}$", line ) == None :
        continue
      print line
    # end for

    ipr = IP4Range( line )
    for ip in ipr:
      if not options.fast:
        time.sleep(1)
      try:
        h = socket.gethostbyaddr( ip )
      except:
        if options.unknown:
          print "%20s %16s %s" % ( line, str( ip ), "unknown" )
        continue
      # end try
      names = h[1]
      names.append(h[0])
      for nam in names:
        if string.find( nam, "in-addr.arpa" ) != -1:
          continue
        # end if
        print "%20s %16s %s" % ( line, str( ip ), nam )
      # end for

    # end for

  # end def
# end class


### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN

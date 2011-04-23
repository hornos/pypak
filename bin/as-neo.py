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

    self.opt( "-k", "--chkpt",
              action = "store", type = "string",
              dest = "chkpt_name", default = "checkpoint",
              help = "Checkpoint" )

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

    self.chkpt = options.chkpt_name
    cline = True
    cip   = True
    try:
      chk = open( self.chkpt, "r" )
    except:
      self.lastip = None
      self.lastline = None
    else:
      (self.lastline, self.lastip) = chk.readline().split( ":" )
      self.lastline = string.strip( self.lastline )
      self.lastip   = string.strip( self.lastip )
      cline = False
      cip   = False
    # end try

    for line in inp.readlines():
      line = string.strip( line )
      if re.match("^([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,3}$", line ) == None :
        continue
      if not self.lastline == None and self.lastline == line :
        cline = True
      if not cline :
        continue
      print " Subnet:%20s" % line

      ipr = IP4Range( line )
      for ip in ipr:
        if not self.lastip == None and self.lastip == ip :
          cip = True
        if not cip :
          continue
        if not options.fast:
          time.sleep(1)
        try:
          h = socket.gethostbyaddr( ip )
        except:
          if options.unknown:
            print "        %20s %20s %s" % ( line, str( ip ), "unknown or failed" )
          self.lastip = ip
          self.lastline = line
          continue
        # end try
        names = h[1]
        names.append(h[0])
        for nam in names:
          if string.find( nam, "in-addr.arpa" ) != -1:
            continue
          # end if
          print "%22s %22s %s" % ( line, str( ip ), nam )
        # end for
        self.lastip = ip
        self.lastline = line
      # end for
    # end for
  # end def
# end class


### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  try:
    p.main()
  except KeyboardInterrupt:
    try:
      fp = open( p.chkpt, "w" )
    except:
      sys.exit( 1 )
    # end try
    fp.write( "%s:%s\n" % ( p.lastline, p.lastip ) )
  # end try
### END MAIN

#!/usr/bin/env python
#TAB: 8
import os
import sys
import string

### BEGIN HEADER
script_name = os.path.basename( sys.argv[0] )
sys.path.append( os.path.dirname( sys.argv[0] ) + "/../lib" )
quantumpack_home   = os.path.dirname( sys.argv[0] ) + "/.."
quantumpack_config = "qppak.ini"
### END HEADER

###
### BEGIN PROGRAM CLASS
###
from QuantumPack.Script import Script
from QuantumPack.FileIO.FileIO import FileIO

class Program( Script ):
  def __init__( self, script_name, quantumpack_home, quantumpack_config ):
    Script.__init__( self, script_name, quantumpack_home, quantumpack_config )

    self.opt_parser.add_option( "-i", "--input",
                         action = "store", type = "string",
                         dest = "input_file", default = "input.UPOT",
                         help = "Input", 
                         metavar="INPUT" )
    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (options, args) = self.opt_parser.parse_args()
    try:
      atomlist  = self.getoptarri( 'atomlist' )
    except:
      print ' Error: no atomlist'
      return 0
    # end try

    # print atomlist

    try:
      reference = self.getopt( 'reference' )
    except:
      reference = None
    # end try

    try:
      origo = self.getoptarrf( 'origo' )
    except:
      origo = nump.zero(3)
    # end try

    try:
      ono = self.getopti( 'ono' )
    except:
      ono = None
    # end try

    try:
      lv = self.getoptarrf( 'lv' )
    except:
      lv = None
    # end try

    try:
      rmin = self.getoptf( 'rmin' )
    except:
      rmin = None
    # end try

    try:
      rmax = self.getoptf( 'rmax' )
    except:
      rmax = None
    # end try


    sysopts = { "verbose" : self.verbose, "debug" : self.debug }
    input_file = options.input_file
    try:
      input_upot = FileIO( input_file, 'UPOT', "r", sysopts )
    except:
      if self.debug:
        raise
      print ' Error: ' + input_file
      return 0
    # end try

    if reference != None :
      try:
        reference_upot = FileIO( reference, 'UPOT', "r", sysopts )
        reference_upot.read()
      except:
        if self.debug:
          raise
        print ' Error: ' + reference
        return 0
      # end try
    # end if
    input_upot.read()
#    if reference != None:
#      input_upot.command( 'reference', { 'reference_upot' : reference_upot } )
#    # end if

    if reference != None:
      ref = reference_upot.handler
    else:
      ref = None
    # end if

    avg_cl_shift = input_upot.command( 'average', { 'atomlist' : atomlist, 
                                                    'lv' : lv, 
                                                    'origo' : origo,
                                                    'reference' : ref,
                                                    'ono' : ono } )
    # end if
    print
    print ' Average Potential:', avg_cl_shift
    print
  # end def main
###
### END PROGRAM CLASS
###


###
### BEGIN MAIN
###
if __name__ == '__main__':
  program = Program( script_name, quantumpack_home, quantumpack_config )
  program.main()
# end if
###
### END MAIN
###

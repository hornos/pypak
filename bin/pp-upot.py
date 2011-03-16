#!/usr/bin/env python
#TAB: 8
import os
import sys
import string

import numpy

### BEGIN HEADER
sys.path.append( os.path.dirname( sys.argv[0] ) + "/../lib" )
### END HEADER

from pypak.Script import Script
from pypak.IO.IO import IO

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
      atomlist  = self.cfgarri( 'atomlist' )
    except:
      print ' Error: no atomlist'
      return 0
    # end try

    try:
      reference = self.cfg( 'reference' )
    except:
      reference = None
    # end try

    try:
      origo_vec = self.cfgarrf( 'origo_vec' )
    except:
      origo_vec = numpy.zeros(3)
    # end try

    try:
      vacancy = self.cfgarri( 'vacancy' )
    except:
      vacancy = None
    # end try

    try:
      lat_vec = self.cfgarrf( 'lat_vec' )
    except:
      lat_vec = None
    # end try


    sysopts = { "verbose" : self.verbose, "debug" : self.debug }
    input_file = options.input_name
    input_upot = IO( input_file, 'UPOT', "r", sysopts )
    input_upot.read()

    ref = None
    if reference != None :
      reference_upot = FIO( reference, 'UPOT', "r", sysopts )
      reference_upot.read()
      ref = reference_upot.handler
    # end if

    avg_cl_shift = input_upot.command( 'average', { 'atomlist'  : atomlist, 
                                                    'lat_vec'   : lat_vec,
                                                    'origo_vec' : origo_vec,
                                                    'vacancy'   : vacancy,
                                                    'reference' : ref } )
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
  p = Program()
  p.main()
# end if
###
### END MAIN
###

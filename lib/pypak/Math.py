#
# Types package
#

import sys
import copy
import string
import numpy as np
import numpy.linalg as npla

def A2F( arr ):
  for i in range( 0, len( arr ) ):
    arr[i] = string.atof( arr[i] )
  # end for
  return np.array( arr )
# end def

def S2F( s ):
  s = s.split()
  return A2F( s )
# end def

def L2N( v ):
  return npla.norm( v )
# end def
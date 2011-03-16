#
# Linear Algebra package
#

from Numeric import *


# Operation: -a
def vec_neg( a = None ):
  for i in range( 0, len( a ) ):
    a[i] = -a[i]
  # end for
  return a
# end def

# Operation
def vector_add( a, b ):
    if len( a ) != len( b ):
	return 0
    
    dim = len( a )
    dvec = zeros( dim, Float )
    
    for i in range( 0, dim ):
	dvec[i] = a[i] + b[i]
    # end for

    return dvec
# end def


# a - b
def vec_sub( a, b ):
  if len( a ) != len( b ):
    raise ValueError( )
    
    dim = len( a )    
    dvec = zeros( dim, Float )
    
    for i in range( 0, dim ):
	dvec[i] = a[i] - b[i]
    # end for
    
    return dvec
# end def


def vector_norm( v ):
    dim = len( v )    

    n = 0.000    
    for i in range( 0, dim ):
	n += v[i] * v[i]
    # end for
    
    return sqrt( n )
# end def


def vector_smul( v, s ):
    dim = len( v )    
    mvec = zeros( dim, Float )

    for i in range( 0, dim ):
	mvec[i] = v[i] * s
    # end for

    return mvec
# end def


def vector_sdiv( v, s ):
    dim = len( v )    
    mvec = zeros( dim, Float )

    for i in range( 0, dim ):
	mvec[i] = v[i] / s
    # end for

    return mvec
# end def


def vector_unit( v ):
    return vector_sdiv( v, vector_norm( v ) )
# end def


def vector_distance( a, b ):
    return vector_norm( vector_sub( a, b ) )
# end def

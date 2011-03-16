import math
import numpy

def v_dr(a,b):
  dr = 0.000
  for i in range(0,3):
    dr += (a[i] - b[i])**2
  # end for
  return math.sqrt(dr)
# end def

#def v_dr2(a,b):
# todo: numpy norm
#  return numpy.linalg.norm( numpy.subtract( a, b ), 'fro' )
# end def

def l_vacancy( target, vac ):
  lookup  = {}
  try:
    vac = sorted( vac )
  except:
    vac = []
  isvac = False
  jj = -1
  i  = 0 # vacancy conuter
  # create lookup table
  for j in target:
    try:
      if j == vac[i]:
        i += 1
        isvac = True
      else:
        jj += 1
      # end if
    except:
      jj += 1
    # end try
    if not isvac:
      lookup[jj] = j
    # end if
    isvac = False
  # end for j
  return lookup
# end def

def m_rmtx( ax = numpy.array([1,0,0]), theta = 0 ):
#  [ xxC+c   xyC-zs  xzC+ys ]
#  [ yxC+zs  yyC+c   yzC-xs ]
#  [ zxC-ys  zyC+xs  zzC+c  ]
  c = math.cos(theta); s = math.sin(theta); C = 1.0 - c
  x = ax[0]; y = ax[1]; z = ax[2]
  m = numpy.zeros([3,3])
  m[0,0] = x * x * C + c
  m[0,1] = x * y * C - z * s
  m[0,2] = x * z * C + y * s
  m[1,0] = y * x * C + z * s
  m[1,1] = y * y * C + c
  m[1,2] = y * z * C - x * s
  m[2,0] = z * x * C - y * s
  m[2,1] = z * y * C + x * s
  m[2,2] = z * z * C + c
  return m
# end def

def v_ang( a, b ):
  return math.acos( numpy.dot( a, b ) )
# end def

import math

def v_dr(a,b):
  dr = 0.000
  for i in range(0,3):
    dr += (a[i] - b[i])**2
  # end for
  return math.sqrt(dr)
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

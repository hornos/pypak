#
# IO Package
# TAB: 4
#
import os
import sys
import string

from QuantumPack.Types import *


class File( Debug ):
  def __init__( self, path = None, opts = "rw" , sysopts = { "verbose" : False, "debug" : False } ):
    Debug.__init__( self, sysopts["verbose"], sysopts["debug"] )
    self.path    = path
    self.opts    = opts
    self.fp      = None
    self.states  = {}
    self.geom    = None
    self.dict    = {}
    self.ibuffer = Buffer()
    self.obuffer = Buffer()
    if string.find( self.opts, "r" ) > -1:
      self.iotype  = IOTypes.Input
      self.buffer  = self.ibuffer
      self.buffer_read()
    else:
      self.iotype  = IOTypes.Output
      self.buffer  = self.obuffer
    # end if
  # end def

  def open( self ):
    print self.path, self.opts
    self.fp = open( self.path, self.opts )
  # end def

  def close( self ):
    self.fp.close()
  # end def

  def io( self, iotype = IOTypes.Input ):
    self.iotype  = iotype
    if self.iotype == IOTypes.Input:
      self.buffer = self.ibuffer
    else:
      self.buffer = self.obuffer
    # end if
  # end def

  def buffer_read( self ):
    self.open()
    self.buffer.read( self.fp )
    self.close()
  # end def
 
  def buffer_write( self ):
    self.open()
    for line in self.buffer.lines:
      self.fp.write( str( self.buffer.lines[line] ) + "\n" )
    # end for
    self.close()
  # end def

  def rewind( self, both = False ):
    if both:
      self.ibuffer.rewind()
      self.obuffer.rewind()
      return
    # end if
    return self.buffer.rewind()
  # end def

  def lc( self ):
    return self.buffer.lc
  # end def

  def getline( self ):
    return self.buffer.getline()
  # end def

  def putline( self, line = None ):
    self.buffer.putline( line )
  # end def

  def line( self ):
    return self.buffer.line.split()
  # end def

  def set( self, key, val ):
    self.dict[key] = val
  # end def

  def state( self, lno, func ):
    self.states[lno] = func
  # end def

  def clean( self ):
    self.states = {}
  # end def

  def comment( self ):
    if self.verbose:
      print " %05d" % self.lc(), "Comment:", self.line()
  # end def

  def skipped( self, detail = "" ):
    if self.verbose and self.debug:
      print " %05d" % self.lc(), "Skipped:", self.line(), detail
  # end def

  def process( self ):
    if self.verbose:
      print " %05d" % self.lc(), "Process:", self.line()
  # end def

  ### begin read
  # seems to be common
  def read_lattice_vectors( self ):
    for i in range( 1, 4 ):
      if i > 1:
        self.getline()
      # end if
      line_arr = self.line()
      for j in range( 0, 3 ):
        self.geom.lattice_vectors[i-1][j] = string.atof(line_arr[j])
      # end for
      self.process()
    # end for
  # end def

  def run( self, limit = 0 ):
    if limit == 0:
      limit = 99999
    # end if
    if self.verbose :
      print " Reading: (%05d)" % limit, self.path
    # end if
    while self.lc() < limit:
      try:
        self.getline()
        try:
          self.states[self.lc()]()
        except Exception as ex:
          if self.verbose:
            self.skipped()
          # end if
          if self.debug:
            print " Exception: " + str( ex )
            # raise
        # end try
      except Exception as ex:
        if self.debug:
          print " Exception: " + str( ex )
          # raise
        break
    # end while
  # end def
  ###  end read

  ### begin write
  ### end write

# end class

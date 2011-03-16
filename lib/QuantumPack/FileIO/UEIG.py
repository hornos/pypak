#
# IO Package
# TAB: 4
#
import os
import sys
import math
import string
import numpy

from QuantumPack.File     import File
from QuantumPack.Types    import *
from QuantumPack.Geometry import Geometry

# UEIG has a fixed format check unified/ueig.F

class FileIO( File ):
  def __init__( self, path = None, opts = "", sysopts = { "verbose" : False, "debug" : False } ):
    File.__init__( self, path, opts, sysopts )
    self.alpha = {}
    self.beta  = {}
  # end def

  def read_nions( self ):
    (nions,nspin) = self.line()
    self.nions = string.atoi( nions )
    self.nspin = string.atoi( nspin )
    self.process()
  # end def


  def read_efermi( self ):
    efermi = self.line()[0]
    self.efermi = string.atof( efermi )
    self.process()
  # end def


  def read_nelect( self ):
    (nelect,nkpts,nbands) = self.line()
    self.nelect = string.atoi( nelect )
    self.nkpts  = string.atoi( nkpts )
    self.nbands = string.atoi( nbands )
    self.process()
  # end def


  def read_bands( self ):
    for i in range(1, self.nkpts + 1):
      # comment
      # print self.line()
      if i > 1:
        self.getline()
        self.getline()
        self.getline()
      # end if
      # self.getline()
      # nk
      self.getline()

      # print self.line()

      (nk,vkpt1,vkpt2,vkpt3,wtkpt) = self.line()
      # comment
      self.getline()
      self.getline()
      (split,spin) = self.line()
      # comment
      self.getline()
      self.getline()
      # bands
      nk = string.atoi(nk)
      self.alpha[nk] = {}
      if self.nspin == 2:
        self.beta[nk] = {}

      for j in range( 1, self.nbands ):
        if j > 1:
          self.getline()
        # end if
        if self.nspin == 2:
          (no,aerg,aocc,berg,bocc) = self.line()
        else:
          (no,aerg,aocc) = self.line()
        # end if
        no = string.atoi( no )
        aerg = string.atof( aerg )
        aocc = string.atof( aocc )
        self.alpha[nk][no] = [aerg,aocc]
        if self.nspin == 2:
          berg = string.atof( berg )
          bocc = string.atof( bocc )
          self.beta[nk][no] = [berg,bocc]
        # end if
        self.process()
      # end for
    # end if
    # print self.alpha
  # end def


  def read( self, opts = None ):
    self.rewind()
    self.clean()
#    self.state( 1, self.comment )
    self.state( 2, self.read_nions )
#    self.state( 3, self.comment )
    self.state( 4, self.read_efermi )
#    self.state( 5, self.comment )
    self.state( 6, self.read_nelect )
#    self.state( 7, self.comment )
#    self.state( 8, self.comment )
    self.state( 8, self.read_bands )
    File.run( self, 8 )
#    self.state( 11 + self.nkpts, self.read_split )
#    self.state( 12 + self.nkpts, self.comment )
#    self.state( 13 + self.nkpts, self.read_bands )
#    File.run( self )
  # end def

  def gauss( self, a = 1.000, x = 0.000, mu = 0.000, sigma = 1.000 ):
    return a * math.exp(-( x - mu ) * ( x - mu ) / ( 2 * sigma * sigma ) )
  # end def

  def eig2dos( self, eigarr = None, alpha = 1.000, sigma = 1.000, channels = 1024 ):
    emin = eigarr[1][0]
    emax = eigarr[self.nbands-1][0]
    eps  = (emax - emin) / channels
    dosarr = numpy.zeros(channels)
    ergarr = numpy.zeros(channels)
    for i in range(1,self.nbands):
      mu = eigarr[i][0]
      
      for j in range(0,channels):
        x = emin + j * eps
        ergarr[j] = x
        dosarr[j] += self.gauss( alpha, x, mu, sigma )
      # end for
    # end for

    return ergarr,dosarr
  # end def


  def gendos( self, argv = None ):
    alpha = argv['alpha']
    sigma = argv['sigma']
    kpt = argv['kpt']
    channels = argv['channels']
    dosarr = [[],[]]

    (ergarr,dosarr[0]) = self.eig2dos( self.alpha[kpt], alpha, sigma, channels )
    fname = './alpha.dos'
    fpdos = open( fname, 'w+' )
    for j in range(0,channels):
      fpdos.write( '%12.6f %12.6f\n' % (ergarr[j],dosarr[0][j] ) )
    # end for
    fpdos.close()
    print fname, 'efermi =',self.efermi

    if self.nspin == 2:
      (ergarr,dosarr[1]) = self.eig2dos( self.beta[kpt], alpha, sigma, channels )
      fname = './beta.dos'
      fpdos = open( fname, 'w+' )
      for j in range(0,channels):
        fpdos.write( '%12.6f %12.6f\n' % (ergarr[j],dosarr[1][j] ) )
      # end for
      fpdos.close()
      print fname, 'efermi =',self.efermi

      fname = './total.dos'
      fpdos = open( fname, 'w+' )
      for j in range(0,channels):
        fpdos.write( '%12.6f %12.6f\n' % (ergarr[j], ( dosarr[0][j] + dosarr[1][j] ) / 2.000  ) )
      # end for
      fpdos.close()

    # end if

  # end def

# end class

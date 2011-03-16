#
# Program
#

import os
from pypak.Script import *
import urwid

class Program( Script ):
  # class vars
  pal = [ ('body', 'black', 'light gray'),
          ('flagged', 'black', 'dark green', ('bold','underline')),
          ('focus', 'light gray', 'dark blue', 'standout'),
          ('flagged focus', 'yellow', 'dark cyan', 
          ('bold','standout','underline')),
          ('head', 'yellow', 'black', 'standout'),
          ('foot', 'light gray', 'black'),
          ('key', 'light cyan', 'black','underline'),
          ('title', 'white', 'black', 'bold'),
          ('dirmark', 'black', 'dark cyan', 'bold'),
          ('flag', 'dark gray', 'light gray'),
          ('error', 'dark red', 'light gray') ]


  def __init__( self, scn = "pypak program", gpc = os.path.dirname( sys.argv[0] )+"/pypak.ini" ):
    Script.__init__( self, scn, gpc )
    self.opt( "-i", "--input", action = "store", type = "string",
              dest = "input_file", default = "input.dat",
              help = "Input", metavar="INPUT" )

    self.htxt = [ ( 'title', scn ) ]
    self.ftxt = [ ( 'key', "ESC - Exit" ) ]

    self.ini()
  # end def


  def gui_exit( self, input ):
    if input == 'esc':
      raise urwid.ExitMainLoop()
  # end def gui_exit

  def input_filter( self, input, raw ):
    return input
  # end def

  def gui_main( self, frame ):
    self.header = urwid.AttrWrap( urwid.Text( self.htxt ), 'head' )
    self.footer = urwid.AttrWrap( urwid.Text( self.ftxt ), 'foot' )
    self.view = urwid.Frame( frame, header = self.header, footer = self.footer )
    loop = urwid.MainLoop( self.view, self.pal, 
           input_filter = self.input_filter,
           unhandled_input = self.gui_exit )
    loop.run()
  # end def gui_main

# end class

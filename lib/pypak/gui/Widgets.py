#
# Program
#

import os
import urwid

class SText( urwid.WidgetWrap ):
  def __init__( self, txt = "SText" ):
    self.text = urwid.Text( txt )
    urwid.WidgetWrap.__init__( self, self.text )
  # end def

  def selectable( self ):
    return True
  # end def

  def keypress( self, size, key ):
    return key
  # end def
  
  def set_text( self, txt ):
    self.text.set_text( txt )
  
  def get_text( self ):
    return self.text.get_text()

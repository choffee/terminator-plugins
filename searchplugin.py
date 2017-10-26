import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import urllib
import terminatorlib.plugin as plugin
import re

# Written by John Cooper http://choffee.co.uk
# Copyright 2010 John Cooper
# See copyright file that comes with this file for full licence

# Modified by cgw 2011/11/06

# AVAILABLE must contain a list of all the classes that you want exposed
AVAILABLE = ['SearchPlugin']

gtk = Gtk

_spaces = re.compile(" +")

# TODO:   move some of the constants into a config object

class SearchPlugin(plugin.Plugin):
    capabilities = ['terminal_menu']

    def do_search(self, searchMenu):
        """Launch Google search for string"""
        if not self.searchstring:
            return
        base_uri = "http://www.google.com/search?q=%s"
        uri = base_uri % urllib.quote(self.searchstring.encode("utf-8"))
        gtk.show_uri(None, uri, Gdk.CURRENT_TIME)
        
    def callback(self, menuitems, menu, terminal):
        """Add our menu item to the menu"""
        self.terminal = terminal
        item = gtk.ImageMenuItem(gtk.STOCK_FIND)
        item.connect('activate', self.do_search)
        if terminal.vte.get_has_selection():
            clip = gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
            self.searchstring = clip.wait_for_text().strip()
            self.searchstring = self.searchstring.replace("\n", " ")
            self.searchstring = self.searchstring.replace("\t", " ")
            self.searchstring = _spaces.sub(" ", self.searchstring)
        else:
            self.searchstring = None
        if self.searchstring:
            if len(self.searchstring) > 40:
                displaystring = self.searchstring[:37] + "..."
            else:
                displaystring = self.searchstring
            item.set_label("Search Google for \"%s\"" % displaystring)
            item.set_sensitive(True)
        else:
            item.set_label("Search Google")
            item.set_sensitive(False)
        # Avoid turning any underscores in selection into menu accelerators
        item.set_use_underline(False)
        menuitems.append(item)

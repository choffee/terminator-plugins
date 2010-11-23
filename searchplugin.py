import gtk
import urllib
import terminatorlib.plugin as plugin


# available must contain a list of all the classes that you want exposed
available = ['SearchPlugin']

class SearchPlugin(plugin.Plugin):
    capabilities = ['terminal_menu']

    def _search(self, searchMenu):
        """Launch google search for string"""
        search = "http://google.co.uk/search?hl=en&q=%s&meta="
        clip = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
        searchstring = clip.wait_for_text()
        uri = search % urllib.quote(searchstring.encode("utf-8"))
        gtk.show_uri(None, uri, gtk.gdk.CURRENT_TIME)



    def callback(self, menuitems, menu, terminal):
        """Add our menu items to the menu"""
        self.terminal = terminal
        item = gtk.ImageMenuItem(gtk.STOCK_FIND)
        item.set_label("Search Online")
        item.connect('activate', self._search)
        item.set_sensitive(terminal.vte.get_has_selection())
        menuitems.append(item)




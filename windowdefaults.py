
import ConfigParser
import os.path

import gtk

import gedit

ui_str = """<ui>
    <menubar name="MenuBar">
        <menu name="EditMenu" action="Edit">
            <menuitem name="UseAsDefault" action="UseAsDefault"/>
        </menu>
    </menubar>
</ui>
"""

ini_path = os.path.expanduser ('~/.gnome2/gedit/WindowDefaults.ini')

class WindowDefaultsPlugin (gedit.Plugin):

    def __init__ (self):
        self.width = None
        self.height = None
        self.windows = dict()
        config = ConfigParser.ConfigParser()
        config.read (ini_path)
        if config.has_option ('geometry', 'width'):
            self.width = config.getint ('geometry', 'width')
        if config.has_option ('geometry', 'height'):
            self.height = config.getint ('geometry', 'height')
        self.disable = True
        gedit.Plugin.__init__(self)
        self.disable = False

    def _insert_ui (self, window):
        manager = window.get_ui_manager()

        action = gtk.Action ('UseAsDefault', 'Use As Default',
            'Set default according to this window', None)
        action.connect ('activate', self._use_as_default, window)

        action_group = gtk.ActionGroup ('WindowDefaults')

        action_group.add_action (action)

        manager.insert_action_group (action_group, -1)

        id_ = manager.add_ui_from_string (ui_str)

        self.windows[window] = (action_group, id_)

    def _remove_ui (self, window):
        (action_group, id_) = self.windows[window]
        del self.windows[window]

        manager = window.get_ui_manager()

        manager.remove_ui (id_)

        manager.remove_action_group (action_group)

        manager.ensure_update()

    def _use_as_default (self, action, window):
        (self.width, self.height) = window.get_size()
        config = ConfigParser.ConfigParser()
        config.add_section ('geometry')
        config.set ('geometry', 'width', self.width)
        config.set ('geometry', 'height', self.height)
        config.write (open (ini_path, 'w'))

    def activate (self, window):
        if self.width is None:
            (self.width, self.height) = window.get_size()
        if not self.disable:
            window.resize (self.width, self.height)
        self._insert_ui (window)

    def deactivate (self, window):
        self._remove_ui (window)


"""Use default settings for newly opened windows instead of copying them frem a previously
opened window."""

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
        """Setup plugin."""

        self.windows = dict()
        config = ConfigParser.ConfigParser()
        config.read (ini_path)
        self._read_config (config)

        # This stops the plugin from resizing all windows when it is enabled from the
        # Preferences dialogue.
        self.disable = True
        gedit.Plugin.__init__(self)
        self.disable = False

    def _read_config (self, config):
        """Read config data from a ConfigParser object."""

        # We will read from the first available window, if these don't exist
        self.width = None
        self.height = None

        if config.has_option ('geometry', 'width'):
            self.width = config.getint ('geometry', 'width')
        if config.has_option ('geometry', 'height'):
            self.height = config.getint ('geometry', 'height')

    def _write_config (self, config):
        """Write config data to a ConfigParser object."""

        config.add_section ('geometry')
        config.set ('geometry', 'width', self.width)
        config.set ('geometry', 'height', self.height)

    def _set_config (self, window):
        """Configure the given window."""

        window.resize (self.width, self.height)

    def _get_config (self, window):
        """Read configuration from the given window."""

        (self.width, self.height) = window.get_size()

    def _insert_ui (self, window):
        """Add plugin user interface to gedit window."""

        manager = window.get_ui_manager()

        action = gtk.Action ('UseAsDefault', 'Use As Default',
            'Set defaults according to this window', None)
        action.connect ('activate', self._use_as_default, window)
        action_group = gtk.ActionGroup ('WindowDefaults')
        action_group.add_action (action)
        manager.insert_action_group (action_group, -1)

        id_ = manager.add_ui_from_string (ui_str)
        self.windows[window] = (action_group, id_)

    def _remove_ui (self, window):
        """Remove plugin user interface from gedit window."""

        (action_group, id_) = self.windows[window]
        del self.windows[window]

        manager = window.get_ui_manager()
        manager.remove_ui (id_)
        manager.remove_action_group (action_group)
        manager.ensure_update()

    def _use_as_default (self, action, window):
        """Read settings from the given window and write them to a file."""

        self._get_config (window)

        config = ConfigParser.ConfigParser()
        self._write_config (config)
        config.write (open (ini_path, 'w'))

    def activate (self, window):
        """Activate plugin for the given window."""

        if self.width is None:
            self._get_config (window)

        if not self.disable:
            self._set_config (window)

        self._insert_ui (window)

    def deactivate (self, window):
        """Deactivate plugin for the given window."""

        self._remove_ui (window)

import gedit

class WindowDefaultsPlugin (gedit.Plugin):

    def __init__ (self):
        self.width = None
        self.height = None
        self.disable = True
        gedit.Plugin.__init__(self)
        self.disable = False

    def activate (self, window):
        if self.width is None:
            (self.width, self.height) = window.get_size()
        if not self.disable:
            window.resize (self.width, self.height)

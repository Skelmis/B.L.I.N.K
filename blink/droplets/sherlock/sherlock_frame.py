import wx

from blink.home_page import DEFAULT_SIZE


class SherlockFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="B.L.I.N.K - Sherlock", size=DEFAULT_SIZE)

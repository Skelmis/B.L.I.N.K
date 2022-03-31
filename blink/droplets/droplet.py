import datetime
from typing import TYPE_CHECKING

import wx

from blink import MenuBar
from blink.constants import DEFAULT_SIZE

if TYPE_CHECKING:
    from blink import HomeFrame


class DropletFrame(wx.Frame):
    def __init__(self, start_time: datetime.datetime, parent=None, title=""):
        super().__init__(parent, title=title, size=DEFAULT_SIZE)

        self.menu_bar: MenuBar = MenuBar(self, start_time, parent)
        self._home_page: "HomeFrame" = parent
        self._start_time: datetime.datetime = start_time

        self.Bind(wx.EVT_CLOSE, self.ensure_close)

    def ensure_close(self, event: wx.Event):
        self.teardown()
        self._home_page.Destroy()

    def teardown(self):
        pass

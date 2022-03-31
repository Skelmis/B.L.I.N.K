import asyncio
import datetime
import time

import humanize
import wx
from wxasync import StartCoroutine


class MenuBar(wx.MenuBar):
    def __init__(self, bind_frame: wx.Frame, start_time: datetime.datetime):
        super().__init__()
        self._start_time: datetime.datetime = start_time

        self.file_menu: wx.Menu = wx.Menu()
        self.file_menu_exit: wx.MenuItem = self.file_menu.Append(
            wx.ID_ANY,
            "Show somethin",
            "Show somethin",
            kind=wx.ITEM_CHECK,
        )
        self.file_menu.Check(self.file_menu_exit.GetId(), True)

        # Add the menubar item to the frame itself
        self.Append(self.file_menu, "&File")
        bind_frame.SetMenuBar(self)

        # Bind buttons to toggles
        bind_frame.Bind(wx.EVT_MENU, self.toggle_somethin, self.file_menu_exit)

        # Adds a bar at the bottom of the screen
        self.status_bar: wx.StatusBar = bind_frame.CreateStatusBar(2)
        self.status_bar.SetStatusText("Ready")
        StartCoroutine(self.update_clock, self)

        # Dynamically size the time status bar bit
        self._bind_frame: wx.Frame = bind_frame
        self.resize_status_bar()

    def toggle_somethin(self, e):
        if self.file_menu_exit.IsChecked():
            self.status_bar.Show()
        else:
            self.status_bar.Hide()

    def resize_status_bar(self):
        time_size = wx.Window.GetTextExtent(self._bind_frame, self.time_now)
        self.status_bar.SetStatusWidths([-1, time_size.width])

    @property
    def time_now(self) -> str:
        time = humanize.precisedelta(
            self._start_time - datetime.datetime.now(tz=datetime.timezone.utc),
        )
        return f"Uptime: {time}"

    async def update_clock(self):
        while True:
            self.status_bar.SetStatusText(self.time_now, 1)
            self.resize_status_bar()
            await asyncio.sleep(1)

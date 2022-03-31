import asyncio
import datetime
import time
from typing import TYPE_CHECKING

import humanize
import wx
from wxasync import StartCoroutine

if TYPE_CHECKING:
    from blink import HomeFrame


class MenuBar(wx.MenuBar):
    def __init__(
        self,
        bind_frame: wx.Frame,
        start_time: datetime.datetime,
        home_page: "HomeFrame",
    ):
        super().__init__()
        self._home_frame: "HomeFrame" = home_page
        self._start_time: datetime.datetime = start_time

        self.navigate_menu: wx.Menu = wx.Menu()
        self.open_home_menu: wx.MenuItem = self.navigate_menu.Append(
            wx.ID_ANY,
            "Home",
            "open_home",
        )

        # Add the menubar item to the frame itself
        self.Append(self.navigate_menu, "Navigate")
        bind_frame.SetMenuBar(self)

        # Bind buttons to toggles
        bind_frame.Bind(wx.EVT_MENU, self.open_home, self.open_home_menu)

        # Adds a bar at the bottom of the screen
        self.status_bar: wx.StatusBar = bind_frame.CreateStatusBar(2)
        self.status_bar.SetStatusText("Ready")
        StartCoroutine(self.update_clock, self)

        # Dynamically size the time status bar bit
        self._bind_frame: wx.Frame = bind_frame
        self.resize_status_bar()

    def open_home(self, event: wx.Event):
        if self._home_frame != self._bind_frame:
            self._bind_frame.Destroy()
            self._home_frame.Show()

    def resize_status_bar(self):
        time_size = wx.Window.GetTextExtent(self._bind_frame, self.time_now)
        self.status_bar.SetStatusWidths([-1, time_size.width])

    def change_status(self, text: str) -> None:
        self.status_bar.SetStatusText(text)

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

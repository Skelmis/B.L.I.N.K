import asyncio

import wx
from wxasync import AsyncBind

from blink import MenuBar

DEFAULT_SIZE = (600, 450)


class HomeFrame(wx.Frame):
    def __init__(self, start_time, parent=None):
        super().__init__(parent, title="B.L.I.N.K", size=DEFAULT_SIZE)

        vbox = wx.BoxSizer(wx.VERTICAL)
        button1 = wx.Button(self, label="Submit")
        self.edit = wx.StaticText(
            self, style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE
        )
        self.edit_timer = wx.StaticText(
            self, style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE
        )
        vbox.Add(button1, 2, wx.EXPAND | wx.ALL)
        vbox.AddStretchSpacer(1)
        vbox.Add(self.edit, 1, wx.EXPAND | wx.ALL)
        vbox.Add(self.edit_timer, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(vbox)
        self.Layout()
        AsyncBind(wx.EVT_BUTTON, self.async_callback, button1)

        # Menubars
        self.menu_bar: MenuBar = MenuBar(self, start_time)

    async def async_callback(self, event):
        self.edit.SetLabel("Button clicked")
        await asyncio.sleep(1)
        self.edit.SetLabel("Working")
        await asyncio.sleep(1)
        self.edit.SetLabel("Completed")

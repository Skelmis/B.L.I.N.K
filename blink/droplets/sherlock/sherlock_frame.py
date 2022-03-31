import datetime

import wx
from wxasync import AsyncBind

from blink.droplets import DropletFrame


class SherlockFrame(DropletFrame):
    def __init__(self, start_time: datetime.datetime, parent=None):
        super().__init__(
            start_time=start_time,
            parent=parent,
            title="B.L.I.N.K - Sherlock",
        )

        self.sizer: wx.BoxSizer = wx.BoxSizer()
        self.input_item: wx.TextCtrl = wx.TextCtrl(self)
        self.sizer.Add(self.input_item)
        self.input_button: wx.Button = wx.Button(self, label="Search")
        self.sizer.Add(self.input_button)
        self.SetSizer(self.sizer)
        self.Layout()

        AsyncBind(wx.EVT_BUTTON, self.do_search, self.input_button)

    async def do_search(self, event: wx.Event):
        """Runs the sherlock search"""
        text: str = self.input_item.GetValue()

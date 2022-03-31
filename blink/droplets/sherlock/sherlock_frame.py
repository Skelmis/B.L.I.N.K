import asyncio
import datetime
import os
from typing import List

import wx
from wxasync import AsyncBind, StartCoroutine

from blink.droplets import DropletFrame
from blink.droplets.sherlock import Sherlock


class SherlockFrame(DropletFrame):
    def __init__(self, start_time: datetime.datetime, parent=None):
        super().__init__(
            start_time=start_time,
            parent=parent,
            title="B.L.I.N.K - Sherlock",
        )
        panel = wx.Panel(self)
        hbox = wx.BoxSizer()

        fgs = wx.FlexGridSizer(2, 2, 9, 25)

        title = wx.StaticText(panel, label="Username")
        review = wx.StaticText(panel, label="Output")

        self.input_button: wx.Button = wx.Button(panel, label="Search")
        self.input_item = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        input_sizer: wx.BoxSizer = wx.BoxSizer()
        input_sizer.Add(self.input_item, 1, wx.EXPAND)
        input_sizer.Add(self.input_button)

        self.output_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        fgs.AddMany(
            [
                (title,),
                (input_sizer, 1, wx.EXPAND),
                (review, 1, wx.EXPAND),
                (self.output_text, 1, wx.EXPAND),
            ]
        )

        fgs.AddGrowableRow(1, 1)
        fgs.AddGrowableCol(1, 1)

        hbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        panel.SetSizer(hbox)

        AsyncBind(wx.EVT_BUTTON, self.do_search, self.input_button)
        AsyncBind(wx.EVT_TEXT_ENTER, self.do_search, self.input_item)

        self._is_currently_searching: bool = False
        self._sherlock: Sherlock = Sherlock(
            os.path.join(os.getcwd(), "blink", "droplets")
        )

    async def do_search(self, event: wx.Event):
        """Runs the sherlock search"""
        if self.is_searching:
            # Can't do concurrent searches
            self.output_text.SetLabel("Cannot do concurrent searches.")
            await asyncio.sleep(2)
            if self.is_searching:
                # Don't override results
                self.output_text.SetLabel("")
            return

        # Clear old output
        self.output_text.SetLabel("")

        # Run search
        self._is_currently_searching = True
        StartCoroutine(self.status_process, self)
        username: str = self.input_item.GetValue()
        if not username:
            self.output_text.SetLabel("Username cannot be nothing.")
            self._is_currently_searching = False
            return

        results: List[str] = await self._sherlock.request(username)

        # Display results
        self._is_currently_searching = False
        self.menu_bar.change_status("Success!")

        for entry in sorted(results, key=len):
            self.output_text.WriteText(f"{entry}\n")

    async def status_process(self):
        i = 1
        while self.is_searching:
            self.menu_bar.change_status("Processing" + "." * i)

            i += 1
            if i == 6:
                i = 1

            await asyncio.sleep(0.5)

    def teardown(self):
        self._is_currently_searching = False

    @property
    def is_searching(self) -> bool:
        return self._is_currently_searching

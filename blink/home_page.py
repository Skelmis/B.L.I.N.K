import asyncio
import datetime

import wx
from wxasync import AsyncBind

from blink import MenuBar
from blink.constants import DEFAULT_SIZE
from blink.droplets.sherlock import SherlockFrame


class HomeFrame(wx.Frame):
    def __init__(self, start_time: datetime.datetime, parent=None):
        super().__init__(parent, title="B.L.I.N.K", size=DEFAULT_SIZE)

        self.menu_bar: MenuBar = MenuBar(self, start_time)
        self._start_time: datetime.datetime = start_time
        """
        wx.Font(pointSize, family, style, weight, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        
        family can be:
        wx.DECORATIVE, wx.DEFAULT,wx.MODERN, wx.ROMAN, wx.SCRIPT or wx.SWISS.
        
        style can be:
        wx.NORMAL, wx.SLANT or wx.ITALIC.
        
        weight can be:
        wx.NORMAL, wx.LIGHT, or wx.BOLD
        """

        # Title panel
        self.title_text: wx.StaticText = wx.StaticText(
            self,
            wx.ID_ANY,
            "B.L.I.N.K",
            style=wx.ALIGN_CENTRE_HORIZONTAL | wx.EXPAND,
        )
        self.title_text.SetFont(
            wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD, wx.TEXT_ATTR_FONT_UNDERLINE)
        )

        # Description
        self.description_text: wx.StaticText = wx.StaticText(
            self,
            wx.ID_ANY,
            "Boldly Jump Into Newfound Knowledge",
        )
        self.description_text.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL))

        # Set size shit
        self.main_sizer: wx.BoxSizer = wx.BoxSizer()

        # Text, top half
        self.text_sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.text_sizer.Add(self.title_text, 1, wx.CENTER)
        self.text_sizer.Add(self.description_text, 1, wx.ALIGN_CENTER | wx.ALIGN_TOP)

        # Options, bottom half
        self.option_sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)

        sherlock_text = "Sherlock\n---------"
        self.sherlock_button: wx.Button = wx.Button(
            self, label=sherlock_text, size=self.GetTextExtent(sherlock_text)
        )
        self.option_sizer.Add(self.sherlock_button, 1, wx.ALIGN_CENTER)

        nest_sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
        nest_sizer.Add(self.text_sizer, 2, wx.CENTER)
        nest_sizer.AddSpacer(10)
        nest_sizer.Add(self.option_sizer, 2, wx.CENTER)

        # Add them to frame
        self.main_sizer.Add(nest_sizer, 3, wx.CENTER)
        self.SetSizer(self.main_sizer)
        self.Layout()

        # Bind events
        AsyncBind(wx.EVT_BUTTON, self.change_to_sherlock, self.sherlock_button)

    async def change_to_sherlock(self, event: wx.Event):
        sf: SherlockFrame = SherlockFrame(self._start_time, self)
        sf.Center()
        sf.Show()
        self.Hide()

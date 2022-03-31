import datetime


from blink.droplets import DropletFrame


class SherlockFrame(DropletFrame):
    def __init__(self, start_time: datetime.datetime, parent=None):
        super().__init__(
            start_time=start_time,
            parent=parent,
            title="B.L.I.N.K - Sherlock",
        )

import asyncio
import datetime
import sys

from wxasync import WxAsyncApp

from blink import HomeFrame

if sys.version_info[1] < 8:
    raise RuntimeError("This package requires python 3.8 or higher.")


async def main():
    start_time: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)

    app = WxAsyncApp()
    frame = HomeFrame(start_time)
    frame.Center()
    frame.Show()

    app.SetTopWindow(frame)
    await app.MainLoop()


asyncio.run(main())

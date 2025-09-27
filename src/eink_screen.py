import time
import logging
from PIL.ImageFile import ImageFile

from waveshare_epd import epd3in52

log = logging.getLogger(__name__)

class EInkScreen:

    def __init__(self):
        logging.info("init and clear")
        self.epd = epd3in52.EPD()
        self.epd.init()
        self.epd.display_NUM(self.epd.WHITE)
        self.epd.lut_GC()
        self.epd.refresh()

        self.epd.send_command(0x50)
        self.epd.send_data(0x17)
        time.sleep(2)


    def update(self, image: ImageFile):
        logging.info("Display image")
        self.epd.display(self.epd.getbuffer(image))
        self.epd.lut_GC()
        self.epd.refresh()


    def shutdown(self):
        logging.info("Clear...")
        self.epd.Clear()
        
        logging.info("Goto Sleep...")
        self.epd.sleep()

        epd3in52.epdconfig.module_exit(cleanup=True)

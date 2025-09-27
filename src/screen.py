import logging
import time
from PIL import Image

log = logging.getLogger(__name__)

try:
    from waveshare_epd import epd3in52
    log.info("E-Ink screen available.")
    from eink_screen import EInkScreen as Screen
except RuntimeError:
    log.warning("No E-Ink screen available. Use dummy screen instead.")
    from dummy_screen import DummyScreen as Screen


def test():
    image = Image.open("test/screen/3in52-1.bmp")

    try:
        screen = Screen()
        screen.update(image)
        time.sleep(10)

    except IOError as e:
        logging.warning("IOError:", str(e))

    except KeyboardInterrupt:    
        screen.shutdown()
        exit()

    screen.shutdown()

if __name__ == "__main__":
    test()

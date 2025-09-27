# IronYard Project

## Setup
Make sure `typst` is installed on the system. Then run:
```
./scripts/build.sh
```

## E-Ink screen for IronYard

### Connection

| e-Paper | BCM2835 encoding | Board physical pin number |
|---------|------------------|---------------------------|
|  VCC 	  |  3.3V 	     |  3.3V                     |
|  GND 	  |  GND 	     |  GND                      |
|  DIN 	  |  MOSI 	     |  19                       |
|  CLK 	  |  SCLK 	     |  23                       |
|  CS 	  |  CE0 	     |  24                       |
|  DC 	  |  25 	     |  22                       |
|  RST 	  |  17 	     |  11                       |
|  BUSY   |  24 	     |  18                       |

### Setup

#### Raspberry Config
```
sudo raspi-config
Select Interfacing Options -> SPI -> Yes to enable the SPI interface
sudo systemctl reboot
```

### Source
https://www.waveshare.com/wiki/3.52inch_e-Paper_HAT_Manual

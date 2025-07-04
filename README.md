# RideSync

## Development

Linux
1. python -m  venv venv (Initial for device)
2. source venv/bin/activate
3. pip install -r requirements.txt

## Configuration for Pi
Connect PI to GPS as following (1-40 | 1 is at the sd slot):

```
           +---------Pi----------+--GPS---+
     3.3V  |  1   2  |  5V       |  5V    | 
     SDA   |  3   4  |  5V       |
     SCL   |  5   6  |  GND      |  GND   |
 GPIO 4    |  7   8  |  TXD      |  RX    |
     GND   |  9  10  |  RXD      |  TX    |
 GPIO 17   | 11  12  |  GPIO 18  |
 GPIO 27   | 13  14  |  GND      |
 GPIO 22   | 15  16  |  GPIO 23  |
     3.3V  | 17  18  |  GPIO 24  |
 MOSI      | 19  20  |  GND      |
 MISO      | 21  22  |  GPIO 25  |
 SCLK      | 23  24  |  CE0      |
     GND   | 25  26  |  CE1      |
 ID_SD     | 27  28  |  ID_SC    |
 GPIO 5    | 29  30  |  GND      |
 GPIO 6    | 31  32  |  GPIO 12  |
 GPIO 13   | 33  34  |  GND      |
 GPIO 19   | 35  36  |  GPIO 16  |
 GPIO 26   | 37  38  |  GPIO 20  |
     GND   | 39  40  |  GPIO 21  |
           +---------------------+--------+
```
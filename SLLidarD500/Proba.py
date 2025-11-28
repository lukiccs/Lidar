import serial
import struct
import Filter
import Parsiranje
import matplotlib.pyplot as plt
import numpy as np
# import Plotovanje

PORT = 'COM10'
BAUDRATE = 230400

prosliUgao = None

with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
    try:
        while True:
            paket = ser.read(46)
            krug = Parsiranje.parsiranje(paket, prosliUgao)
            if krug is False:
                pass
                
            else: 
                print(krug)
                prosliUgao = krug[-1][1]
            # Parsiranje.proba()
    except KeyboardInterrupt:
        print("GOTOVO")
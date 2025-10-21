import serial
import struct
import Filter
import Parsiranje
import matplotlib.pyplot as plt
import numpy as np

PORT = 'COM10'
BAUDRATE = 230400

# ====================================
# plt.ion()
# fig = plt.figure(figsize=(6,6))
# ax = plt.subplot(111, polar=True)
# sc = ax.scatter([], [], s=10, c='lime', alpha=0.7)
# ax.set_ylim(0, 2000)
# ax.set_theta_zero_location('N')
# ax.set_theta_direction(-1)
# ax.set_title("Waveshare D500 – Real-time radar view", fontsize=12)
# =====================================
x = []
y = []
with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
    try:
        while True:
            paket = ser.read(46)
            uredjeniParovi = Parsiranje.parsiranje(paket)
            if uredjeniParovi is not None:
                print('Rastojanja i uglovi:')
                print(uredjeniParovi)
                print('==============================')
                uglovi = []
                ugloviRad = []
                rastojanja = [] 
                prethodniUgao = None
                ugloviKrug = []
                rastojanjaKrug = []
                for ugao, rastojanje in uredjeniParovi:
                    if prethodniUgao is not None and ugao < prethodniUgao:
                        uglovi.clear()
                        ugloviRad.clear()
                        print('==============NOVI KRUG=================')

                    uglovi.append(ugao)
                    ugloviRad.append(np.deg2rad(ugao))
                    rastojanja.append(rastojanje)
                    prethodniUgao = uglovi[-1]
                    # x.append(rastojanje * np.cos(np.deg2rad(ugao)))
                    # y.append(rastojanje * np.sin(np.deg2rad(ugao)))
                # print('UGLOVI:')
                # print(uglovi, prethodniUgao)
                # print('==============================')
    except KeyboardInterrupt:
        print("GOTOVO")
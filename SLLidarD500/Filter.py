import serial
import struct

def filtriranjeDistanci(ocitanaMerenja):
    # Filtriranje distanci koje su manje od 20mm ili veće od 5000mm
    for i in range(len(ocitanaMerenja)):
        if ocitanaMerenja[i] < 20 or ocitanaMerenja[i] > 5000:
            ocitanaMerenja.pop(i)
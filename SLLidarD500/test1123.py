import serial
import struct
import math
import Filter

PORT = 'COM10'
BAUDRATE = 230400
brojTacaka = 12

def procitaj_paket(ser):
    """Čeka dok ne pronađe validan heder (0x54 0x2C) i pročita ceo paket od 90 bajtova."""
    # Traži heder
    while True:
        bajt = ser.read(1)
        if bajt == b'\x54':  # Prvi bajt
            drugi = ser.read(1)
            if drugi == b'\x2C':  # Drugi bajt
                ostatak = ser.read(88)  # već smo pročitali 2
                return b'\x54\x2C' + ostatak

def izracunaj_uglove(start_angle, end_angle, brojTacaka):
    """Linearna interpolacija između start i end ugla."""
    razlika = end_angle - start_angle
    if razlika < 0:
        razlika += 360  # ako pređe nulu
    korak = razlika / brojTacaka
    return [(start_angle + i * korak) % 360 for i in range(brojTacaka)]

with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
    try:
        prethodni_ugao = None
        ceo_krug = []

        while True:
            paket = procitaj_paket(ser)

            if len(paket) == 90:
                start_angle = struct.unpack('<H', paket[4:6])[0] / 100.0
                offset = 6
                ocitanaMerenja = []

                for i in range(brojTacaka):
                    distance = struct.unpack('<H', paket[offset:offset+2])[0]
                    confidence = paket[offset + 2]
                    ocitanaMerenja.append(distance)
                    offset += 3

                # End angle
                end_angle_offset = 6 + brojTacaka * 3
                end_angle = struct.unpack('<H', paket[end_angle_offset:end_angle_offset+2])[0] / 100.0

                # Ugao svake tačke
                uglovi = izracunaj_uglove(start_angle, end_angle, brojTacaka)

                # Dodaj tačke u ceo krug
                for a, d in zip(uglovi, ocitanaMerenja):
                    ceo_krug.append((a, d))

                # Detekcija kraja kruga
                if prethodni_ugao is not None and start_angle < prethodni_ugao:
                    print("=== CELOKUPAN KRUG ===")
                    print(f"Broj tačaka: {len(ceo_krug)}")
                    print(ceo_krug[:14], "...")  # prikaz samo prvih 14 da ne zatrpa
                    print("=======================")
                    ceo_krug.clear()

                prethodni_ugao = start_angle

                # Debug info za svaki paket
                print(f"Start: {start_angle:.2f}°, End: {end_angle:.2f}°, Tacke: {ocitanaMerenja}")

    except KeyboardInterrupt:
        print("GOTOVO")
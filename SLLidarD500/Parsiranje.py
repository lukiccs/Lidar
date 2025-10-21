import serial
import struct
import Filter

global start_angle, end_angle
brojTacaka = 12


def parsiranje(paket):
    ocitanaRastojanja = []
    uredjeniParovi = []
    uglovi = []
    if len(paket) == 46 and paket[0] == 0x54 and paket[1] == 0x2C:
                    start_angle = struct.unpack('<H', paket[4:6])[0] / 100.0
                    offset = 6
                    for i in range(brojTacaka):
                        distance = struct.unpack('<H', paket[offset:offset+2])[0]
                        confidence = paket[offset + 2]
                        ocitanaRastojanja.append(distance)
                        offset += 3
                    end_angle = struct.unpack('<H', paket[offset:offset+2])[0] / 100.0

                    korakInterpolacijeUgla  = (end_angle - start_angle + 360) % 360 / (brojTacaka - 1)
                    uglovi = [(start_angle + i * korakInterpolacijeUgla) % 360 for i in range(brojTacaka)]
                    uredjeniParovi = list(zip(uglovi, ocitanaRastojanja))
                    return uredjeniParovi

import serial
import struct
import Plotovanje
import Alati

global start_angle, end_angle
brojTacaka = 12

def parsiranje(paket, prosliUgao):
    global krug
    krug = []
    ocitanaRastojanja = []
    if len(paket) == 46 and paket[0] == 0x54 and paket[1] == 0x2C:
                  start_angle = struct.unpack('<H', paket[4:6])[0] / 100.0
                  offset = 6
                  for i in range(brojTacaka):
                        # citanje tacaka
                        distance = struct.unpack('<H', paket[offset:offset+2])[0]
                        confidence = paket[offset + 2]
                        ocitanaRastojanja.append(distance)
                        offset += 3
                        end_angle = struct.unpack('<H', paket[offset:offset+2])[0] / 100.0

                        korakInterpolacijeUgla  = (end_angle - start_angle + 360) % 360 / (brojTacaka - 1)


                  
                        # ugao = (start_angle + i * korakInterpolacijeUgla) % 360
                        # if prosliUgao is None:
                        #       krug.append((distance, ugao))
                        #       prosliUgao = ugao
                        # if ugao < prosliUgao:
                        #       krug.clear()
                        #       print("-----------------NOVI KRUG!--------------------")
                        #       krug.append((distance, ugao))
                        # elif ugao >= prosliUgao:
                        #       krug.append((distance, ugao))
                        # prosliUgao = ugao


                  for i, ugao in enumerate(ocitanaRastojanja):
                        ugao = (start_angle + i * korakInterpolacijeUgla) % 360
                        if prosliUgao is None:
                              krug.append((ocitanaRastojanja[i], ugao))
                              prosliUgao = ugao
                        if ugao < prosliUgao:
                              krug.clear()
                              print("-----------------NOVI KRUG!--------------------")
                              krug.append((ocitanaRastojanja[i], ugao))
                        elif ugao > prosliUgao:
                              krug.append((ocitanaRastojanja[i], ugao))
                        prosliUgao = ugao
                        
                  return krug





def proba():
    for r, theta in krug:
        x, y = Alati.polarUDekart(r, theta)
        Plotovanje.sredjivanjePlot(x, y)
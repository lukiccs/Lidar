import serial
import struct
import matplotlib.pyplot as plt

def parse_packet(packet):
    global end_angle, start_angle, count
    if len(packet) != 90:
        return None

    if packet[0] != 0x54 or packet[1] != 0x2C:
        return None  # Not a valid packet

    count = packet[3]
    start_angle = struct.unpack('<H', packet[4:6])[0] / 100.0

    measurements = []
    offset = 6
    for i in range(count):
        distance = struct.unpack('<H', packet[offset:offset+2])[0]
        confidence = packet[offset + 2]
        measurements.append((distance, confidence))
        offset += 3

    end_angle = struct.unpack('<H', packet[offset:offset+2])[0] / 100.0

    # Angle interpolation per sample
    angle_diff = (end_angle - start_angle + 360) % 360
    angle_step = angle_diff / max(count - 1, 1)

    angles = [(start_angle + i * angle_step) % 360 for i in range(count)]

    return list(zip(angles, measurements))

# -------------------- Main Serial Reader --------------------

PORT = 'COM10'  # <- Change this to match your port
BAUDRATE = 230400

with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
    try:
        while True:
            packet = ser.read(90)
            result = parse_packet(packet)
            if result:
                for angle, (distance, confidence) in result:
                    print(f"Angle: {angle:.2f}°, Distance: {distance} mm, Confidence: {confidence}, startAngle = {start_angle:.2f}, endAngle = {end_angle:.2f}, count = {count}")
                print("-" * 50)
    except KeyboardInterrupt:
        print("Stopped.")

plt.ion()  # interaktivni mod da se graf ažurira u realnom vremenu
if result:
    for angle, (distance, confidence) in result:
        print(f"Angle: {angle:.2f}°, Distance: {distance} mm, Confidence: {confidence}, startAngle = {start_angle:.2f}, endAngle = {end_angle:.2f}, count = {count}")
    print("-" * 50)
        # --- Plotovanje u polarnim koordinatama ---
    import numpy as np
    plt.clf()  # obriši prethodni plot
    angles = [np.deg2rad(a) for a, _ in result]
    distances = [d for _, (d, _) in result]
    ax = plt.subplot(111, projection='polar')
    ax.scatter(angles, distances, s=5, c='b')
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    plt.pause(0.01)

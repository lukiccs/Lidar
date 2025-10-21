import serial
import struct
from collections import defaultdict


# provera i parsiranje paketa
# proverava validnost paketa
def parse_packet(packet):
    global count
    if len(packet) != 90 or packet[0] != 0x54 or packet[1] != 0x2C:
        return None

    count = packet[3]
    start_angle = struct.unpack('<H', packet[4:6])[0] / 100.0

    measurements = []
    offset = 6
    for _ in range(count):
        distance = struct.unpack('<H', packet[offset:offset+2])[0]
        confidence = packet[offset + 2]
        measurements.append((distance, confidence))
        offset += 3

    end_angle = struct.unpack('<H', packet[offset:offset+2])[0] / 100.0

    angle_diff = (end_angle - start_angle + 360) % 360
    angle_step = angle_diff / max(count - 1, 1)
    angles = [(start_angle + i * angle_step) % 360 for i in range(count)]

    return list(zip(angles, measurements))


def bin_measurements(measurements, bin_size=15):
    bins = defaultdict(list)

    for angle, (distance, confidence) in measurements:
        if distance == 0 or confidence < 50:
            continue
        # Round to the nearest bin
        bin_index = int((angle + bin_size / 2) // bin_size) * bin_size % 360
        bins[bin_index].append(distance)

    averaged = {}
    for b in range(0, 360, bin_size):
        dists = bins.get(b, [])
        avg = sum(dists) / len(dists) if dists else None
        averaged[b] = avg

    return averaged



# ---------------- Main Serial Reader ----------------

PORT = 'COM10'  # <-- Change this to your actual port
BAUDRATE = 230400

with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
    try:
        while True:
            packet = ser.read(90)
            parsed = parse_packet(packet)
            if not parsed:
                continue

            binned = bin_measurements(parsed)
            print(f"Distance readings (every 15°), count:{count}:")
            for angle in range(0, 360, 15):
                d = binned.get(angle)
                if d:
                    print(f"{angle:>3}°: {d:.1f} mm")
                else:
                    print(f"{angle:>3}°: No data")
            print("-" * 50)

    except KeyboardInterrupt:
        print("Stopped.")

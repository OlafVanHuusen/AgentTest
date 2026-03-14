import wave
import struct
import math
import os


def generate_sound(filepath, duration_seconds=1, frequency=440, sample_rate=22050):
    num_samples = int(duration_seconds * sample_rate)
    
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            t = i / sample_rate
            value = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * t))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)


def generate_ambient(filepath, duration_seconds=5, sample_rate=22050):
    import random
    num_samples = int(duration_seconds * sample_rate)
    
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            t = i / sample_rate
            low_freq = 60 + 20 * math.sin(2 * math.pi * 0.1 * t)
            value = int(32767 * 0.15 * (
                0.5 * math.sin(2 * math.pi * low_freq * t) +
                0.3 * math.sin(2 * math.pi * (low_freq * 1.5) * t) +
                0.2 * math.sin(2 * math.pi * (low_freq * 2) * t)
            ))
            value += int(32767 * 0.02 * random.uniform(-1, 1))
            value = max(-32768, min(32767, value))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)


def generate_thunder(filepath, duration_seconds=3, sample_rate=22050):
    import random
    num_samples = int(duration_seconds * sample_rate)
    
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            t = i / sample_rate
            envelope = math.exp(-3 * t) * (1 - math.exp(-20 * t))
            noise = random.uniform(-1, 1)
            rumble = 0.5 * math.sin(2 * math.pi * 40 * t) + 0.3 * math.sin(2 * math.pi * 60 * t)
            value = int(32767 * 0.5 * envelope * (0.7 * noise + 0.3 * rumble))
            value = max(-32768, min(32767, value))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)


def main():
    sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("Generating sound files...")
    generate_sound(os.path.join(sounds_dir, 'bus_engine.wav'), duration_seconds=3, frequency=80)
    print("  - bus_engine.wav")
    
    generate_ambient(os.path.join(sounds_dir, 'ambient.wav'), duration_seconds=5)
    print("  - ambient.wav")
    
    generate_thunder(os.path.join(sounds_dir, 'thunder.wav'), duration_seconds=3)
    print("  - thunder.wav")
    
    print("Done!")


if __name__ == '__main__':
    main()

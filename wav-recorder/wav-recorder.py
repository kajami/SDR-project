import pyaudio
import wave
from datetime import datetime

p = pyaudio.PyAudio()  # Create an interface to PortAudio

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second

frames = []  # Initialize array to store frames

# Create filename for saved .wav-file
date_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
filename = f"./recordings/recording-{date_time}.wav"

print('Recording...')
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

# Store data until keyboard interrupt (ctrl + c)
try:
	while True:
		data = stream.read(chunk)
		frames.append(data)
except KeyboardInterrupt:
	print("Finished recording")
except Exception as e:
	print(str(e))

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
import pyaudio
import threading
import wave

class Recorder:
    def __init__(self):
        self.frames = []
        self.recording = False
    def _record(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        while self.recording:
            data = stream.read(CHUNK)
            self.frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def start_recording(self):
        self.recording = True
        self.frames = []
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        self.thread.join()


    def save_to_file(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()
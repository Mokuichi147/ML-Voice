from enum import Enum
import numpy as np
import pyaudio
import simpleaudio
import wave


class ReadMode(Enum):
    NONE = 0
    MIC = 1
    FILE = 2


class AudioWave:
    def __init__(
            self,
            read_mode: ReadMode = ReadMode.NONE,
            mic_device_index: int = 0,
            load_file_path: str = 'input.wav',
            save_file_path: str = 'output.wav',
            sampling_rate: int = 44100,
            chunk: int = 1024,
            channels: int = 1
            ):
        # mic or file
        self.read_mode = read_mode
        # mic setting
        self.mic_device_index = mic_device_index
        # file setting
        self.load_file_path = load_file_path
        self.save_file_path = save_file_path
        # wave setting
        self.sampling_rate = sampling_rate
        self.chunk = chunk
        self.channels = channels
        # other
        self.is_mic_opened:        bool = False
        self.is_file_read_opened:  bool = False
        self.is_file_write_opened: bool = False
        self.pyaudio_object = pyaudio.PyAudio()
        self.pyaudio_stream = None
        self.wave_read      = None
        self.wave_write     = None


    def set_mic_from_devicename(self, device_name: str):
        _device_index = self.mic_device_index
        for device_index in range(self.pyaudio_object.get_device_count()):
            device_info = self.pyaudio_object.get_device_info_by_index(device_index)
            if device_name in device_info['name']:
                _device_index = device_index
                break
        self.mic_device_index = _device_index


    def read_close(self):
        if self.is_mic_opened:
            self.pyaudio_stream.close()
            self.is_mic_opened = False
        if self.is_file_read_opened:
            self.wave_read.close()
            self.is_file_read_opened = False

    def write_close(self):
        if self.is_file_write_opened:
            self.wave_write.close()
            self.is_file_write_opened = False

    def close(self):
        self.read_close()
        self.write_close()
    
    def write_and_close(self, audio_wave):
        if self.read_mode == ReadMode.MIC:
            self.write(audio_wave)
        self.close()


    def read_open(self):
        if self.read_mode == ReadMode.MIC and not self.is_mic_opened:
            self.pyaudio_stream = self.pyaudio_object.open(
                format = pyaudio.paInt16,
                channels = self.channels,
                rate = self.sampling_rate,
                frames_per_buffer = self.chunk,
                input_device_index = self.mic_device_index,
                input = True,
                output = False
            )
            self.is_mic_opened = True
        elif self.read_mode == ReadMode.FILE and not self.is_file_read_opened:
            self.wave_read = wave.open(self.load_file_path, 'rb')
            self.is_file_read_opened = True

    def write_open(self):
        if not self.is_file_write_opened:
            self.wave_write = wave.open(self.save_file_path, 'wb')
            self.wave_write.setnchannels(self.channels)
            # 16bit == 2byte
            self.wave_write.setsampwidth(2)
            self.wave_write.setframerate(self.sampling_rate)
            self.wave_write.setcomptype('NONE', 'not compressed')
            self.is_file_write_opened = True
    
    def open(self):
        self.read_open()
        self.write_open()


    def change_readmode(self, read_mode: ReadMode, is_open: bool = True):
        if self.read_mode == read_mode:
            return
        elif self.is_mic_opened or self.is_file_read_opened:
            self.read_close()

        self.read_mode = read_mode
        if is_open:
            self.read_open()


    def read(self, listen: bool = False) -> np.ndarray:
        audio_wave = np.array([], dtype=np.int16)
        if self.read_mode == ReadMode.MIC and self.is_mic_opened:
            buf = self.pyaudio_stream.read(self.chunk, exception_on_overflow=False)
            audio_wave = np.frombuffer(buf, dtype=np.int16)
        elif self.read_mode == ReadMode.FILE and self.is_file_read_opened:
            buf = self.wave_read.readframes(self.chunk)
            audio_wave = np.frombuffer(buf, dtype=np.int16)
        if listen:
            self.listen(audio_wave)
        return audio_wave

    def write(self, audio_wave: np.ndarray):
        if not self.is_file_write_opened:
            self.write_open()
        self.wave_write.setnframes(audio_wave.shape[0])
        self.wave_write.writeframes(audio_wave.tobytes())
    
    def listen(self, audio_wave: np.ndarray):
        simpleaudio.play_buffer(audio_wave, self.channels, 2, self.sampling_rate)
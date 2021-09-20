from audiowave import AudioWave, ReadMode
import numpy as np


file_name = input('File names (e.g. test.wav): ')
mic_device_name = input('Microphone Device Name (e.g. WebCam): ')
recording_time = float(input('Recording time (e.g. 3.5): '))


AW = AudioWave(
    read_mode = ReadMode.MIC,
    save_file_path = file_name,
    chunk = 1470
    )
if mic_device_name != '':
    AW.set_mic_from_devicename(mic_device_name)

AW.read_open()
signal_all = np.array([], dtype=np.int16)


count = 0
while count < (AW.sampling_rate / AW.chunk) * recording_time:
    signal = AW.read()
    signal_all = np.concatenate([signal_all, signal], 0)
    count += 1


AW.listen(signal_all)
AW.write(signal_all)
AW.close()
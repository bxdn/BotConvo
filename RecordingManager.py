import struct
import wave
import keyboard
from pvrecorder import PvRecorder


class RecordingManager:
    """
    Manages speech recognition logic
    """

    def __init__(self, settings):
        self._OUT_FILE = settings.get('temp_file_name', default='out.wav')
        print('Speech Recognition Ready...')

    def record_audio(self):
        """
        Gets a message from the user's mic (user must press ctrl)
        :return: the message string
        """
        recorder = PvRecorder(512)
        recorder.start()
        frames = []
        print('Hold \'ctrl\' to speak a message.')
        keyboard.wait('ctrl')
        while keyboard.is_pressed('ctrl'):
            frames.extend(recorder.read())
        recorder.delete()
        with wave.open(self._OUT_FILE, 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(frames), *frames))
        return self._OUT_FILE

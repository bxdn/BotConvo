
from time import sleep
import struct
import wave
import keyboard
from pvrecorder import PvRecorder


class RecordingManager:
    """
    Manages speech recognition logic
    """

    def __init__(self):
        print('Speech Recognition Ready...')

    @staticmethod
    def record_audio():
        """
        Gets a message from the user's mic (user must press ctrl)
        :return: the message string
        """
        recorder = PvRecorder(512)
        recorder.start()
        frames = []
        print('Hold \'ctrl\' to speak a message.')
        while not keyboard.is_pressed('ctrl'):
            sleep(0.01)
        print('Recording...')
        while keyboard.is_pressed('ctrl'):
            frames.extend(recorder.read())
        recorder.delete()
        with wave.open('tmp.wav', 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(frames), *frames))
        print("Done Recording!")
        return 'tmp.wav'

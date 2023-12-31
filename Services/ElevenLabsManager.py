
from queue import Queue
from threading import Thread
from time import sleep

from elevenlabs import generate, set_api_key, voices, play


class ElevenLabsManager:
    """
    Manages Eleven Labs communications
    """
    def __init__(self, settings):
        set_api_key(settings.EL_API_KEY)

        self._VOICES = voices()
        self._VOICE_STABILITY = settings.get('el', default={}).get('voice_stability', 0.5)
        self._VOICE_SIMILARITY = settings.get('el', default={}).get('voice_similarity', 0.8)

        self._to_generate = Queue()
        self._to_play = Queue()

        Thread(target=self._listen_for_messages).start()
        Thread(target=self._listen_for_audio).start()

        print('Eleven Labs Ready...')

    def say_response(self, response_to_speak, voice_name):
        """
        Using the predefined voice, will say the response into the user's speakers using ElevenLab's API
        Additionally, if MPV is installed, will stream to reduce latency, otherwise, will just play once it's done
        :param voice_name: The Eleven labs voice name to speak the message
        :param response_to_speak: The string to speak
        """
        voice = self._get_voice(voice_name)
        voice.settings.stability = self._VOICE_STABILITY
        voice.settings.similarity_boost = self._VOICE_SIMILARITY
        self._to_generate.put({'message': response_to_speak, 'voice': voice})

    def _listen_for_messages(self):
        while True:
            if self._to_generate.qsize():
                to_generate = self._to_generate.get()
                self._to_play.put(generate(
                    text=to_generate['message'],
                    voice=to_generate['voice']
                ))
            else:
                sleep(0.05)

    def _listen_for_audio(self):
        while True:
            if self._to_play.qsize():
                to_play = self._to_play.get()
                play(to_play, use_ffmpeg=False)
            else:
                sleep(0.05)

    def _get_voice(self, voice_name):
        matches = [voice for voice in self._VOICES if voice.name == voice_name]
        if not matches:
            raise ValueError("Matching voice not found!")
        return [voice for voice in self._VOICES if voice.name == voice_name][0]

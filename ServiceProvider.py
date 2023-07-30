
from ElevenLabsManager import ElevenLabsManager
from OpenAIManager import OpenAIManager
from RecordingManager import RecordingManager
from oai_functions.FunctionProvider import FunctionProvider


class ServiceProvider:
    def __init__(self, settings):
        self._settings = settings

        if settings.get('voice') or settings.get('voice1') and settings.get('voice2'):
            self._el_service = ElevenLabsManager(settings)

        if settings.get('mic'):
            self._recording_service = RecordingManager()

        if self._settings.get('use_funcs'):
            assert self._settings.mode == 'user_bot', 'Function calling is not compatible with bot_bot mode'
            self._function_service = FunctionProvider(self)

        self._oai_service = OpenAIManager(settings, self)

    def settings(self):
        return self._settings

    def oai_service(self):
        return self._oai_service

    def el_service(self):
        return self._el_service

    def recording_service(self):
        return self._recording_service

    def function_service(self):
        return self._function_service

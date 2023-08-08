
from Services.ElevenLabsManager import ElevenLabsManager
from Services.OpenAIManager import OpenAIManager
from Services.RecordingManager import RecordingManager
from Services.FunctionProvider import FunctionProvider


class ServiceProvider:
    """
    Provides services to apps and other services where necessary
    """
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
        """
        Gets the settings
        @return: the settings
        """
        return self._settings

    def oai_service(self):
        """
        Gets the OpenAI service
        @return: the OpenAI service
        """
        return self._oai_service

    def el_service(self):
        """
        Gets the ElevenLabs service
        @return: the ElevenLabs service
        """
        return self._el_service

    def recording_service(self):
        """
        Gets the Recording service
        @return: the Recording service
        """
        return self._recording_service

    def function_service(self):
        """
        Gets the Function service
        @return: the Function service
        """
        return self._function_service

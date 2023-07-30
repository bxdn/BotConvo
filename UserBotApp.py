
import os

from App import App
from ElevenLabsManager import ElevenLabsManager
from OpenAIManager import OpenAIManager
from RecordingManager import RecordingManager


class UserBotApp(App):
    """
    Class for having a conversation between the user and the bot.
    """
    def __init__(self, settings):
        super().__init__(settings)
        self._instruct_message = settings.instruct
        self._voice = settings.voice
        self._mic = settings.mic

        self._oai_manager = OpenAIManager(settings)
        if self._voice:
            self._el_manager = ElevenLabsManager(settings)
        if self._mic:
            self._r_manager = RecordingManager()

    def run(self):
        """
        Starts chat mode with ChatGPT
        :param voice: Name of Eleven Labs voice to use if
        :param instruct_message: The message telling ChatGPT what it is, before the chat starts
        :param mic: Whether to get user message from mic or keyboard
        """
        if self._read_history:
            self._init_history_file()
        else:
            self._messages.append({'role': 'system', 'content': self._instruct_message})
        print('App Running!')
        while True:
            self._send_and_receive()

    def _send_and_receive(self):
        user_message = self._get_message()
        if self._mic:
            print(f'YOU: {user_message}')
        self._messages.append({"role": "user", "content": user_message})
        response, function_name, function_output = self._oai_manager.get_response(self._messages, self._get_send_and_receive_callback(self._voice))
        while function_name:
            if response:
                self._messages.append({'role': 'assistant', 'content': response})
            self._messages.append({'role': 'function', 'name': function_name, 'content': function_output})
            response, function_name, function_output = self._oai_manager.get_response(self._messages,
                                                                                      self._get_send_and_receive_callback(
                                                                                          self._voice))
        if response:
            self._messages.append({'role': 'assistant', 'content': response})
        print()

    def _get_message(self):
        if not self._mic:
            return input('Input next message.\nYOU: ')
        file_name = self._r_manager.record_audio()
        with open(file_name, 'rb') as file:
            to_ret = self._oai_manager.transcribe(file)
        os.remove(file_name)
        return to_ret


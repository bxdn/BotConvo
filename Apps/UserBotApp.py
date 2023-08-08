
import os

from Apps.App import App


class UserBotApp(App):
    """
    Class for having a conversation between the user and the bot.
    """
    def __init__(self, service_provider):
        super().__init__(service_provider)
        self._instruct_message = service_provider.settings().instruct
        self._voice = service_provider.settings().voice
        self._mic = service_provider.settings().get('mic')

    def run(self):
        """
        Starts chat mode with ChatGPT
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
        self._messages.append({"role": "user", "content": user_message})
        response, function_name, function_output = self._service_provider.oai_service().get_response(self._messages, self._get_send_and_receive_callback(self._voice))
        while function_name and not response:
            self._messages.append({'role': 'function', 'name': function_name, 'content': function_output})
            response, function_name, function_output = self._service_provider.oai_service().get_response(self._messages, self._get_send_and_receive_callback(self._voice))
        if function_name:
            self._messages.append({'role': 'function', 'name': function_name, 'content': function_output})
        if response:
            self._messages.append({'role': 'assistant', 'content': response})
        print()

    def _get_message(self):
        if not self._mic:
            return input('Input next message.\n')
        file_name = self._service_provider.recording_service().record_audio()
        with open(file_name, 'rb') as file:
            to_ret = self._service_provider.oai_service().transcribe(file)
        os.remove(file_name)
        print(to_ret)
        return to_ret

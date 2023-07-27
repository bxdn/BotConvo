
from App import App
from ElevenLabsManager import ElevenLabsManager
from OpenAIManager import OpenAIManager


class BotBotApp(App):
    """
    Runs a conversation between two bots
    """
    def __init__(self, settings):
        super().__init__(settings)

        self._oai_manager = OpenAIManager(settings)
        if settings.voice1 and settings.voice2:
            self._el_manager = ElevenLabsManager(settings)
        elif settings.voice1 or settings.voice2:
            raise ValueError('Voices must either both be utilized or not at all!')

    def run(self):
        """
        Runs the chat
        """
        print('App Running!')
        self._handle_initial_message()
        instruct_message = self._settings.instruct1
        voice = self._settings.voice1
        while True:
            instruct_message = self._settings.instruct1 if instruct_message == self._settings.instruct2 else self._settings.instruct2
            voice = self._settings.voice1 if voice == self._settings.voice2 else self._settings.voice2
            self._transform_messages(instruct_message)
            self._get_next_bot_message(voice)

    def _handle_initial_message(self):
        self._messages.append({'role': 'system', 'content': self._settings.instruct1})
        self._messages.append({'role': 'assistant', 'content': self._settings.initial_message})
        print(f'BOT: {self._settings.initial_message}')
        if self._settings.voice1:
            self._el_manager.say_response(self._settings.initial_message, self._settings.voice1, True)

    def _get_next_bot_message(self, voice):
        response = self._oai_manager.get_response(self._messages, self._get_send_and_receive_callback(voice))
        override = input('\nPress enter to continue.  If you would like to override the last message, Type it here.\n')
        if override:
            response = override
        self._messages.append({'role': 'assistant', 'content': response})

    def _transform_messages(self, new_instruct_message):
        for message in self._messages:
            role = message['role']
            if role == 'system':
                message['content'] = new_instruct_message
            elif role == 'user':
                message['role'] = 'assistant'
            else:
                message['role'] = 'user'

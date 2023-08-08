
from Apps.App import App


class BotBotApp(App):
    """
    Runs a conversation between two bots
    """

    def run(self):
        """
        Runs the chat
        """
        if self._read_history:
            self._init_history_file()
        else:
            self._handle_initial_message()
        instruct_message = self._service_provider.settings().instruct1
        voice = self._service_provider.settings().voice1
        print('App Running!')
        while True:
            instruct_message = self._service_provider.settings().instruct1 \
                if instruct_message == self._service_provider.settings().instruct2 \
                else self._service_provider.settings().instruct2
            voice = self._service_provider.settings().voice1 \
                if voice == self._service_provider.settings().voice2 \
                else self._service_provider.settings().voice2
            self._transform_messages(instruct_message)
            self._get_next_bot_message(voice)

    def _handle_initial_message(self):
        self._messages.append({'role': 'system', 'content': self._service_provider.settings().instruct1})
        self._messages.append({'role': 'assistant', 'content': self._service_provider.settings().initial_message})
        print(self._service_provider.settings().initial_message)
        if self._service_provider.settings().voice1:
            self._service_provider.el_service().say_response(
                self._service_provider.settings().initial_message, self._service_provider.settings().voice1
            )

    def _get_next_bot_message(self, voice):
        callback = self._get_send_and_receive_callback(voice)
        response = self._service_provider.oai_service().get_response(self._messages, callback)[0]
        override = input('''
            \n\nPress enter to continue.  If you would like to override the last message, Type it here.\n
        ''')
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

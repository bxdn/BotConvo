
import sys
from abc import ABC, abstractmethod
from json import dumps, loads

from keyboard import add_hotkey


class App(ABC):
    """
    A chat application
    """

    def __init__(self, service_provider):
        self._service_provider = service_provider
        self._messages = []
        self._read_history = service_provider.settings().get('read_history')
        add_hotkey('ctrl+d', self._exit)

    @abstractmethod
    def run(self):
        """
        Runs the application
        """

    def _exit(self):
        if self._service_provider.settings().get('write_history'):
            with open(self._service_provider.settings().write_history, 'w') as history_file:
                history_file.write(dumps({'messages': self._messages}))
        sys.exit()

    def _init_history_file(self):
        with open(self._read_history, 'r') as history_file:
            self._messages = loads(history_file.read())['messages']

    def _get_send_and_receive_callback(self, voice):
        def _send_and_receive_callback(message):
            print(message, end='', flush=True)
            if voice:
                self._service_provider.el_service().say_response(message, voice)

        return _send_and_receive_callback

import sys
from abc import ABC, abstractmethod
from json import dumps, loads

from keyboard import add_hotkey


class App(ABC):
    """
    A chat application
    """

    def __init__(self, settings):
        self._settings = settings
        self._el_manager = None
        self._oai_manager = None
        self._r_manager = None
        self._messages = []
        self._read_history = settings.get('read_history')
        add_hotkey('ctrl+d', self._exit)

    @abstractmethod
    def run(self):
        """
        Runs the application
        """

    def _exit(self):
        if self._settings.get('write_history'):
            with open(self._settings.write_history, 'w') as history_file:
                history_file.write(dumps({'messages': self._messages}))
        sys.exit()

    def _init_history_file(self):
        with open(self._read_history, 'r') as history_file:
            self._messages = loads(history_file.read())['messages']

    def _get_send_and_receive_callback(self, voice):
        def _send_and_receive_callback(message, first):
            if first:
                print('BOT: ', end='')
            print(message, end='', flush=True)
            if voice:
                self._el_manager.say_response(message, voice, first)

        return _send_and_receive_callback

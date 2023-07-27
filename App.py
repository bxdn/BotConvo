
from abc import ABC, abstractmethod


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

    @abstractmethod
    def run(self):
        """
        Runs the application
        """

    def _get_send_and_receive_callback(self, voice):
        def _send_and_receive_callback(message, first):
            if first:
                print('BOT: ', end='')
            print(message, end='', flush=True)
            if voice:
                self._el_manager.say_response(message, voice, first)
        return _send_and_receive_callback

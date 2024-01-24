from threading import Thread
from time import sleep

from oai_functions.FunctionModule import FunctionModule


class TimeFuncs(FunctionModule):
    """
    Function module for time-related stuff
    """
    def _set_timer(self, args):

        def _timer():
            sleep(args['seconds'])
            self._service_provider.el_service().say_response('BEEP, BEEP, BEEP!!', self._service_provider.settings().voice)

        Thread(target=lambda: _timer()).start()
        return f"Timer Set for {args['seconds']} seconds."

    def get_funcs(self):
        """
        Gets the function dictionary
        """
        return {'set_timer': self._set_timer}

    def get_function_descriptions(self):
        """
        Gets the function descriptors
        """
        return [
            {
                "name": "set_timer",
                "description": "Sets a timer for n seconds.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "seconds": {
                            "type": "integer",
                            "description": "The amount of seconds on the timer",
                        }
                    },
                    "required": ["seconds"]
                }
            }
        ]

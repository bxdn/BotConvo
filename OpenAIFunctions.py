from threading import Thread
from time import sleep
from playsound import playsound


def _set_timer(args):
    print(f"Timer Set for {args['seconds']} seconds.")

    def _timer():
        sleep(args['seconds'])
        playsound('alarm.mp3')

    Thread(target=lambda: _timer()).start()
    return 'Timer is set!'


functions = {
    'set_timer': _set_timer
}
function_descriptions = [
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

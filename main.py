
from dynaconf import Dynaconf

from BotBotApp import BotBotApp
from UserBotApp import UserBotApp

def run():
    """
    Run the App.
    """
    settings = Dynaconf(settings_files=['settings.yml'])
    if settings.mode == 'bot_bot':
        app = BotBotApp(settings)
    elif settings.mode == 'user_bot':
        app = UserBotApp(settings)
    else:
        raise ValueError('Unknown run mode specified in settings file!')
    app.run()


if __name__ == '__main__':
    run()

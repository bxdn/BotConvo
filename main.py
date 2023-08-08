
from dynaconf import Dynaconf

from Apps.BotBotApp import BotBotApp
from Services.ServiceProvider import ServiceProvider
from Apps.UserBotApp import UserBotApp


def run():
    """
    Run the App.
    """
    settings = Dynaconf(settings_files=['settings.yml'])
    service_provider = ServiceProvider(settings)
    if settings.mode == 'bot_bot':
        app = BotBotApp(service_provider)
    elif settings.mode == 'user_bot':
        app = UserBotApp(service_provider)
    else:
        raise ValueError('Unknown run mode specified in settings file!')
    app.run()


if __name__ == '__main__':
    run()

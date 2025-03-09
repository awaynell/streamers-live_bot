from telegram.ext import ContextTypes


def getVKLiveStreamers(context: ContextTypes.DEFAULT_TYPE = None):
    return context.chat_data.get("vklivestreamers", [])


def setVKLiveStreamers(streamers: list, context: ContextTypes.DEFAULT_TYPE = None):
    context.chat_data['vklivestreamers'] = streamers


class Settings:
    def __init__(self, context: ContextTypes.DEFAULT_TYPE = None):
        self.vklivestreamers = context.chat_data.get("vklivestreamers", [])
        self.kickstreamers = []
        self.update_interval = 60
        self.context = context

    def getUpdateInterval(self):
        return self.update_interval

    def setUpdateInterval(self, interval):
        self.update_interval = interval

    def getVkLiveStreamers(self):
        return self.vklivestreamers


def getSettings(context: ContextTypes.DEFAULT_TYPE = None):
    return Settings(context=context)

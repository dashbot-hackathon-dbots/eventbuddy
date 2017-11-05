from microsoftbotframework import MsBot
from tasks import MessageHandler

bot = MsBot()
bot.add_process(MessageHandler.handle_message)

if __name__ == '__main__':
    bot.run()

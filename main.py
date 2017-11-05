from microsoftbotframework import MsBot
from tasks import handle_message

bot = MsBot()
bot.add_process(handle_message)

if __name__ == '__main__':
    bot.run()
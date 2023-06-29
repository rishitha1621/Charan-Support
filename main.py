## --> Don't try to steal or experiment. This is prod


from source import telegram_bot
import replit_keep_alive

if __name__ == "__main__":
    bot_instance = telegram_bot.MafiaBot()
    replit_keep_alive.WaitressStart("Hello World")
    bot_instance.run()


## --> Don't try to steal or experiment.. This is prod
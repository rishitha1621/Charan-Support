## --> Don't try to steal or experiment. This is production


from source import telegram_bot
import replit_keep_alive


if __name__ == "__main__":
    bot_instance = telegram_bot.MafiaBot()
    replit_keep_alive.WaitressStart("Charan ka Mafia................")
    bot_instance.run()


## --> Don't try to steal or experiment.. This is production
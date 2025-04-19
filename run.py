import multiprocessing

from bot.run_bot import bot_main



if __name__ == "__main__":

    bot_process = multiprocessing.Process(target=bot_main)
    bot_process.start()
    bot_process.join()
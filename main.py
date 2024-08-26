import schedule
import time
from app.scraper import check_bookings_for_passport
from app.telegram import bot
from app.logger import logger
from app.config import Config
from datetime import datetime
import pytz

# Set the timezone to Guayaquil (UTC-5)
guayaquil_tz = pytz.timezone('America/Guayaquil')


def check_and_notify(verbose: bool = True):
    now = datetime.now(guayaquil_tz) 
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    if verbose:
        logger.info(f'- consultando consulado [{now_str}]')

    are_there_bookings = check_bookings_for_passport(take_screenshots=False, headless=True, browserless=True)
    if are_there_bookings:
        bot.send_message(Config.TELEGRAM_CHAT_ID, "Hola, he detectado disponibilidad de citas. Probablemente sea un buen momento para revisar la página web del consulado.")


def run_schedule(only_night = True, start = 22, end = 6, delay: int = 60, every_minutes: int = 30, notify_on_first: bool = True, notify_on_last: bool = True):
    now = datetime.now(guayaquil_tz) 
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Bot iniciado [{now_str}]")
    if notify_on_first:
        bot.send_message(Config.TELEGRAM_CHAT_ID, "Saludos, quería comunicarte que estoy operativo.")
    
    first_check = True
    last_check = False

    schedule.every(every_minutes).minutes.do(check_and_notify) 

    while True:
        now = datetime.now(guayaquil_tz)  # Use the Guayaquil timezone
        is_in_time = now.hour >= start or now.hour < end

        #  run every 30 minutes
        if only_night and is_in_time:
            if first_check:
                bot.send_message(Config.TELEGRAM_CHAT_ID, "Queria avisarte que he empezado mi jornada. 😎")
                first_check = False      

            if now.hour == end - 1 and now.minute >= every_minutes:  # Check if it's the last check of the night
                last_check = True
            
        if last_check:
            bot.send_message(Config.TELEGRAM_CHAT_ID, "Ha sido una larga noche. Voy a dormir. 🥱😴")
            last_check = False
            first_check = True  # Reset for the next night

        schedule.run_pending()
        time.sleep(delay)


if __name__ == "__main__":
    run_schedule()
    # check_bookings_for_passport(headless=False, browserless=False)
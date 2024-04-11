import logging
import os

from util import dialogue

logger = logging.getLogger(__name__)

env_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(env_dir, '.env')

def create_env_file():
    # Check if .env file exists
    if not os.path.exists(env_file):
        # If not, create it
        with open(env_file, 'w') as f:
            pass

def load_env_variables():
    # Load environment variables from .env file
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip():
                key, value = line.strip().split('=')
                os.environ[key] = value

def save_env_variable(key, value):
    # Save environment variable to .env file
    with open(env_file, 'a') as f:
        f.write(f"{key}={value}\n")           

def check():
    # Check if .env file exists
    if not os.path.exists(env_file):
        create_env_file()

    load_env_variables()

    shown = False
    # Define required environment variables
    if not os.environ.get('TEMP_DOWNLOAD_PATH'):
        if not shown:
            logger.warning('It looks like this is your first time running the Music Video Downloader, or you are missing some environment variables.  Either way let\'s set them up now.')
            shown = True
        logger.info('We need to setup a temporary path for downloaded files to live.')
        while True:
            user_input = dialogue.query('Required', 'Enter the absolute path of your temp directory')
            if not os.path.exists(user_input):
                logger.warning('The input path does not exist.  Try again...')
            else:
                break
        save_env_variable('TEMP_DOWNLOAD_PATH', user_input)
        logger.info('Temp directory saved as {}', user_input)
        load_env_variables()

    if not os.environ.get('LIBRARY_PATH'):
        if not shown:
            logger.warning('It looks like this is your first time running the Music Video Downloader, or you are missing some environment variables.  Either way let\'s set them up now.')
            shown = True
        logger.info('We need to know where you would like to keep your videos, the directory path will house folders for each Artist.')
        while True:
            user_input = dialogue.query('Required', 'Enter the absolute path of your media directory')
            if not os.path.exists(user_input):
                logger.warning('The input path does not exist.  Try again...')
            else:
                break
        save_env_variable('LIBRARY_PATH', user_input)
        logger.info('Media directory saved as {}', user_input)
        load_env_variables()

    if not os.environ.get('IMVD_KEY'):
        if not shown:
            logger.warning('It looks like this is your first time running the Music Video Downloader, or you are missing some environment variables.  Either way let\'s set them up now.')
            shown = True
        logger.info('You must register an app with the Internet Music Video Database (IMVDb) and use that API Key to get Music Videos.')
        logger.info('To register visit - https://imvdb.com/developers/api and click "Register New App"')
        while True:
            user_input = dialogue.query('Required', 'Enter the IMVDb API Key')
            if not imvd.test(user_input):
                logger.warning('That IMVDb API Key does not seem to work.  Try again...')
            else:
                break
        save_env_variable('IMVD_KEY', user_input)
        logger.info('IMVDb API Key saved as {}', user_input)
        load_env_variables()
        

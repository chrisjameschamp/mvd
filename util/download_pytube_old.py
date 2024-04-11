import logging
import os
import random
import re
import string

from datetime import datetime
from pytube import YouTube
from tqdm import tqdm
from util import imvd, mover

logger = logging.getLogger(__name__)

class VideoDownloader:
    def __init__(self):
        self.pbar = None
        self.filename = None
        self.duration = 0

    def progress_callback(self, stream, chunk, bytes_remaining):
        self.pbar.update(len(chunk))

    def download_video(self, video, add_code=False):
        vender = None
        code = None
        fail = False
        for source in video['sources']:
            if source['is_primary']:
                vender = source['source']
                code = source['source_data']
        if vender == 'youtube':
            url = f'http://youtube.com/watch?v={code}'
            try:
                logger.info(f'Downloading {url}...')
                yt = YouTube(url, on_progress_callback=self.progress_callback)
                stream = yt.streams.get_highest_resolution()
                self.duration = yt.length
                self.pbar = tqdm(total=stream.filesize, unit='B', unit_scale=True, desc='[DOWN]')
                track_artists = imvd.artists(video['artists'])
                now = datetime.now()
                date_time_str = now.strftime('%Y%m%d%H%M%S')
                if add_code:
                    if video['year']:
                        self.filename = mover.sanitize_filename(f'{", ".join(track_artists)} - {video["song_title"]} {self.generate_random_code()} ({video["year"]})_{date_time_str}.mp4')
                    else:
                        self.filename = mover.sanitize_filename(f'{", ".join(track_artists)} - {video["song_title"]} {self.generate_random_code()}_{date_time_str}.mp4')
                else:
                    if video['year']:
                        self.filename = mover.sanitize_filename(f'{", ".join(track_artists)} - {video["song_title"]} ({video["year"]})_{date_time_str}.mp4')
                    else:
                        self.filename = mover.sanitize_filename(f'{", ".join(track_artists)} - {video["song_title"]}_{date_time_str}.mp4')
                stream.download(output_path=os.environ['TEMP_DOWNLOAD_PATH'],filename=self.filename)
            except Exception as e:
                logger.error('Failed to download video: {}', e)
                fail = True
            finally:
                if self.pbar is not None:
                    self.pbar.close()
                if not fail:
                    logger.info('Download Successful')
                    return [f'{os.environ['TEMP_DOWNLOAD_PATH']}/{self.filename}', self.duration]
                else:
                    return False

    def generate_random_code(self):
        # Define the characters to choose from: uppercase letters and digits
        characters = string.ascii_uppercase + string.digits
        # Use random.choices to pick 4 characters, then join them into a string
        code = ''.join(random.choices(characters, k=4))
        return code

    def extract_video_id(self, youtube_url):
        # Regex pattern to match different YouTube URL formats
        pattern = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
        else:
            return None
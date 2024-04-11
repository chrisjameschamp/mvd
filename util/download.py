import logging
import random
import os
import re
import string
import yt_dlp

from datetime import datetime
from tqdm import tqdm
from util import imvd, mover

logger = logging.getLogger(__name__)

class VideoDownloader:
    def __init__(self):
        self.pbar = None
        self.filename = None
        self.duration = 0
        self.downloaded = 0

    def progress_callback(self, info_dict):
        status = info_dict.get('status')
        if status in ('downloading', 'finished'):
            if status == 'downloading':
                if self.pbar is None:
                    total_bytes = info_dict.get('total_bytes')
                    if total_bytes:
                        self.pbar = tqdm(total=total_bytes, unit='B', unit_scale=True, desc='[DOWN]')
                    else:
                        self.pbar = tqdm(unit='B', unit_scale=True, desc='[DOWN]')
                else:
                    chunk = info_dict.get('downloaded_bytes') - self.downloaded
                    self.downloaded = info_dict.get('downloaded_bytes')
                    self.pbar.update(chunk)
            elif status == 'finished':
                if self.pbar:
                    self.pbar.close()
        elif status == 'error':
            raise ExceptionType(info_dict.get('error'))

    def download_video(self, video, add_code=False):
        vender = None
        code = None
        fail = False
        for source in video['sources']:
            if source['is_primary']:
                vender = source['source']
                code = source['source_data']

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
        file_path = os.path.join(os.environ['TEMP_DOWNLOAD_PATH'], self.filename)

        ## YOUTUBE
        if vender == 'youtube':
            url = f'http://youtube.com/watch?v={code}'
            try:
                logger.info(f'Downloading {url}...')
                ydl_opts = {
                    'progress_hooks': [self.progress_callback],
                    'format': 'best',
                    'outtmpl': file_path,
                    'noplaylist': True,
                    'merge_output_format': 'mp4',
                    'logger': None,
                    'quiet': True,  # Suppress yt-dlp's stdout messages
                    'noprogress': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.download(url)
                logger.info('Download Successful')
                return [file_path, self.duration]
            except Exception as e:
                logger.error('Failed to download video: {}', e)
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
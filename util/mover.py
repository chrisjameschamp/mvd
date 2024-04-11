import logging
import re
import os

from tqdm import tqdm

logger = logging.getLogger(__name__)

def move(video_file, subtitle_file, artist):
    try:
        logger.info('Preparing to move temp files...')
        folder_dir = os.path.join(os.environ['LIBRARY_PATH'], artist)
        if not os.path.exists(folder_dir):
            logger.info('Folder for artist does not exist.  Creating {}...', folder_dir)
            os.makedirs(folder_dir, exist_ok=True)
            logger.debug('Folder {} created', folder_dir)
        else:
            logger.debug('Folder {} exists', folder_dir)
        os.makedirs(folder_dir, exist_ok=True)
        os.chmod(folder_dir, 0o777)

        src_dir, video = os.path.split(video_file)
        src_dir, subtitle = os.path.split(subtitle_file)

        video_new_filename = "_".join(video.split("_")[:-1]) + ".mp4"
        subtitle_new_filename = "_".join(subtitle.split("_")[:-1]) + ".ass"

        video_new_path = f'{folder_dir}/{video_new_filename}'
        subtitle_new_path = f'{folder_dir}/{subtitle_new_filename}'

        logger.info('Moving video file to {}...', folder_dir)
        logger.debug('New file path: {}', video_new_path)
        move_file_with_progress(video_file, video_new_path)
        logger.info('Move successful')
        logger.info('Moving subtitle file to {}...', folder_dir)
        logger.debug('New file path: {}', subtitle_new_path)
        move_file_with_progress(subtitle_file, subtitle_new_path)
        logger.info('Move successful')
        return [video_new_path, subtitle_new_path]
    except Exception as e:
        logger.error('Failed to move files: {}', e)
        return False

def move_file_with_progress(src_path, dst_path, buffer_size=256*256):
    total_size = os.path.getsize(src_path)
    with tqdm(total=total_size, unit='B', unit_scale=True, desc='[MOVE]') as pbar:
        with open(src_path, 'rb') as src_file:
            with open(dst_path, 'wb') as dst_file:
                while True:
                    chunk = src_file.read(buffer_size)
                    if not chunk:
                        break
                    dst_file.write(chunk)
                    pbar.update(len(chunk))
    os.chmod(dst_path, 0o777)
    os.remove(src_path)

def check_for_file(video, track_artists):
    if video['year']:
        file_name = sanitize_filename(f'{", ".join(track_artists)} - {video["song_title"]} ({video["year"]}).mp4')
    else:
        file_name = sanitize_filename(f'{", ".join(track_artists)} - {video["song_title"]}.mp4')
    file_path = os.path.join(os.environ['LIBRARY_PATH'], track_artists[0], file_name)
    if os.path.exists(file_path):
        return True
    else:
        return False

def sanitize_filename(filename):
    # Define a regular expression pattern for characters you want to replace
    # This includes /, \, :, and non-printable ASCII characters
    pattern = r'[\/\\:]+|[\x00-\x1f\x7f]'
    # Replace these characters with an underscore
    safe_filename = re.sub(pattern, '_', filename)
    # Optional: Prevent files from being hidden by leading dot
    if safe_filename.startswith('.'):
        safe_filename = '_' + safe_filename[1:]
    return safe_filename
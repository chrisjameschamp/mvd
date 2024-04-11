import logging
import os

logger = logging.getLogger(__name__)

def add_to_playlist(files, artist, title):
    try:
        logger.info('Updating Playlist...')
        playlist = []
        track_info = None
        playlist_file = os.path.join(os.environ['LIBRARY_PATH'], 'Playlist.m3u')

        logger.debug('Opening playlist file {}...', playlist_file)
        with open(playlist_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#EXTINF:'):
                    # If there's existing track info, add it to the playlist before starting a new one
                    if track_info:
                        playlist.append(track_info)
                    # Extract metadata (duration and title)
                    _, metadata = line.split('#EXTINF:', 1)
                    duration, etitle = metadata.split(',', 1)
                    track_info = {'duration': duration, 'title': etitle, 'paths': []}
                elif not line.startswith('#') and line:
                    # Add the path to the current track info's list of paths
                    if track_info:
                        track_info['paths'].append(line)
            playlist.append(track_info)

        playlist.append({'duration': -1, 'title': f'{artist} - {title}', 'paths': [files[0], files[1]]})
        logger.info('Added {} - {} to the playlist', artist, title)
        logger.debug('Saving playlist {}...', playlist_file)
        with open(playlist_file, 'w') as file:
            file.write('#EXTM3U\n')
            for track in playlist:
                file.write(f"#EXTINF:{track['duration']},{track['title']}\n")
                for path in track['paths']:
                    file.write(f"{path}\n")
        logger.info('Successfully updated playlist')
        return True
    except Exception as e:
        logger.error('Failed to update playlist file: {}', e)
        return False

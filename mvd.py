#!/usr/bin/env python3

import logging
import sys

DEBUG = False

if __name__ == '__main__':
    from util import colargulog, constants, dialogue, env

    console_handler = logging.StreamHandler(stream=sys.stdout)
    colored_formatter = colargulog.ColorizedArgsFormatter(constants.TERMINAL_FORMAT, constants.TERMINAL_DATE_FMT)
    console_handler.setFormatter(colored_formatter)
    if DEBUG:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger()
    logger.name = 'MVD'
    logger.addHandler(console_handler)

    dialogue.intro()
    env.check()

    from util import download, imvd, mover, playlist, subtitle

    try:
        while True:
            logger.info('Select a function from the list:')
            logger.info('   {}) Search the Internet Music Video Database', 1)
            logger.info('   {}) Manually Add Youtube Video', 2)
            logger.info('   {}) Exit', 3)
            option = dialogue.query('Numeric', 'Select a value 1-3', min=1, max=3)
            if int(option)==1:
                query = dialogue.query('Required', 'Search terms')
                results = imvd.search(query)
                if results:
                    logger.info('   {}) Select All', 1)
                    for i, result in enumerate(results):
                        track_artists = imvd.artists(result['artists'])
                        logger.info('   {}) {} - {}, {}', i+2, ', '.join(track_artists), result['song_title'], result['year'])
                    selects = dialogue.query('Required', 'Select which videos you would like to download.\nFor multiple entries seperate them by a comma.')
                    selects = imvd.parse_string_to_list(selects)
                    if 1 in selects:
                        selects = [i for i in range(2, 2 + len(results))]
                    downloader = download.VideoDownloader()
                    for select in selects:
                        choice = select-2
                        if choice > len(results):
                            logger.warn('Select {} is out of range of the available options. Skipping select...', select)
                            continue
                        track_artists = imvd.artists(results[select-2]['artists'])
                        logger.info('Preparing download of {} - {}...', f'{", ".join(track_artists)}', results[select-2]['song_title'])
                        video = imvd.get_video(results[select-2]['id'])
                        if not video['year']:
                            logger.warning('No year is defined for {} - {}', f'{", ".join(track_artists)}', results[select-2]['song_title'])
                            year = dialogue.query('Numeric', 'Enter the year the video is from:', min=1900, max=2100, default=None)
                            video['year'] = year
                        if mover.check_for_file(video, track_artists):
                            logger.warning('Video already exists for {} - {}', f'{", ".join(track_artists)}', results[select-2]['song_title'])
                            user_input = dialogue.query('Y/N', 'Would you like to download anyway (y/N)?', default='N')
                            if user_input.casefold().startswith('n'):
                                logger.info('Skipping {} - {}', f'{", ".join(track_artists)}', results[select-2]['song_title'])
                                continue
                            else:
                                downloaded_video = downloader.download_video(video, add_code=True)
                        else:
                            downloaded_video = downloader.download_video(video)
                        if downloaded_video:
                            st = subtitle.create_subtitle_file(downloaded_video[0], f'{", ".join(track_artists)}', results[select-2]['song_title'], results[select-2]['year'], downloaded_video[1])
                            if st:
                                result = mover.move(downloaded_video[0], st, track_artists[0])
                                if result:
                                    success = playlist.add_to_playlist(result, ', '.join(track_artists), results[select-2]["song_title"])
                        logger.info('----')
                else:
                    logger.warning('No search results for {}. Try another search term.', query)
            elif int(option)==2:
                youtube_url = dialogue.query('Required', 'Enter the URL of the youtube video.')
                downloader = download.VideoDownloader()
                youtube_id = downloader.extract_video_id(youtube_url)
                logger.info('Using youtube id: {}', youtube_id)
                artist = dialogue.query('Required', 'Enter the track Artist.')
                title = dialogue.query('Required', 'Enter the track Title.')
                year = dialogue.query('Numeric', 'Enter the year the video is from:', min=1900, max=2100, default=None)
                logger.info('Preparing download of {} - {}...', artist, title)
                downloader = download.VideoDownloader()
                video = {
                    'sources': [
                        {
                            'source': 'youtube',
                            'is_primary': True,
                            'source_data': youtube_id
                        }
                    ],
                    'artists': [
                        {
                            'name': artist
                        }
                    ],
                    'song_title': title,
                    'year': year
                }
                track_artists = imvd.artists(video['artists'])
                if mover.check_for_file(video, track_artists):
                    logger.warning('Video already exists for {} - {}', f'{", ".join(track_artists)}', title)
                    user_input = dialogue.query('Y/N', 'Would you like to download anyway (y/N)?', default='N')
                    if user_input.casefold().startswith('n'):
                        logger.info('Skipping {} - {}', f'{", ".join(track_artists)}', title)
                        continue
                    else:
                        downloaded_video = downloader.download_video(video, add_code=True)
                else:
                    downloaded_video = downloader.download_video(video)
                if downloaded_video:
                    st = subtitle.create_subtitle_file(downloaded_video[0], f'{", ".join(track_artists)}', title, year, downloaded_video[1])
                    if st:
                        result = mover.move(downloaded_video[0], st, track_artists[0])
                        if result:
                            success = playlist.add_to_playlist(result, f'{", ".join(track_artists)}', title)
                logger.info('----')
            elif int(option)==3:
                logger.info('Exiting...')
                sys.exit()
        logger.info(' ')
    except Exception as e:
        logger.error('{}', e)
    except KeyboardInterrupt:
        logger.info('Exiting...')
    finally:
        sys.exit()

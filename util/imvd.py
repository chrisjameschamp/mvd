import logging
import os
import re

import requests
import urllib.parse

from util import constants

logger = logging.getLogger(__name__)

headers = {
        "IMVDB-APP-KEY": os.environ['IMVD_KEY'],
        "Accept": "application/json"
    }

def search(query):
    logger.debug('Searching the Internet Music Video Database for search term: {}', query)
    results = []
    page = 1
    while True:
        url = f"{constants.IMVD_API}/search/videos?q="
        response = api_call(url, query, page)
        if (response):
            if response['total_pages']>0:
                for result in response['results']:
                    results.append(result)
                if response['total_pages']==page:
                    break
                page += 1
            else:
                return False
        else:
            logger.error('IMVDb API seems to be offline.  Try again later')
            return False
    return results

def test(api_key):
    logger.debug('Testing IMVDb API Key: {}', api_key)
    url = f"{constants.IMVD_API}/entity/634"
    test_headers = {
        "IMVDB-APP-KEY": api_key,
        "Accept": "application/json"
    }
    response = requests.get(url, headers=test_headers)
    if response.status_code == 200:
        return True
    else:
        logger.error(response.status_code)
        return False

def get_video(id):
    logger.info('Pulling video data for IMVDB entry id: {}', id)
    url = f"{constants.IMVD_API}/video/{id}?include=sources"
    response = api_call(url, '')
    return response


def api_call(func, query, page=0):
    query = urllib.parse.quote_plus(query)
    if page > 0:
        url = f"{func}{query}&page={page}"
    else:
        url = f"{func}{query}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(response.status_code)
        return False

def artists(artists):
    track_artists = []
    for artist in artists:
        track_artists.append(str(artist['name']))
    return track_artists

def is_valid_format(s):
    pattern = re.compile(r'^\s*\d+(\s*-\s*\d+)?(\s*,\s*\d+(\s*-\s*\d+)?)*\s*$')
    return bool(pattern.match(s))

def parse_string_to_list(s):
    if not is_valid_format(s):
        raise ValueError("Selects contains invalid characters. Only numbers, commas, and dashes are allowed.")

    elements = []
    for part in s.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            elements.extend(range(start, end + 1))
        else:
            elements.append(int(part))
    return elements
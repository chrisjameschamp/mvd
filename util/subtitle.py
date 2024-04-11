import logging

logger = logging.getLogger(__name__)

def create_subtitle_file(video_path, artist, title, year, duration):
    '''Create an ASS subtitle file with specified text at the beginning and end of the video.'''
    logger.info('Creating subtitle file for {} - {}...', artist, title)
    try:
        subtitle_path = video_path.rsplit('.', 1)[0] + '.ass'
        
        # Setup for ASS file
        ass_header = (
            '[Script Info]\n'
            'ScriptType: v4.00+\n'
            'ScaledBorderAndShadow: yes\n'
            'PlayResX: 1024\n'
            'PlayResY: 768\n'
            '\n'
            '[V4+ Styles]\n'
            'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, '
            'Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, '
            'Alignment, MarginL, MarginR, MarginV, Encoding\n'
            'Style: Default,DejaVu Sans,34,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n'
            '\n'
            '[Events]\n'
            'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
        )

        with open(subtitle_path, 'w') as f:
            f.write(ass_header)
            
            # Subtitle at the start of the video
            if year:
                subtitle = f'{artist}\\N"{title}"\\N{year}\\NLength: {format_duration(duration, True)}'
            else:
                subtitle = f'{artist}\\N"{title}"\\NLength: {format_duration(duration, True)}'
            f.write(f'Dialogue: 0,00:00:00.00,00:00:06.00,Default,,0,0,0,,{{\\an1\\fad(500,500)}}{subtitle}\n')
            
            # Subtitle at the end of the video
            end_start = duration - 6
            end_start_formatted = format_duration(end_start)
            total_time_formatted = format_duration(duration)
            f.write(f'Dialogue: 0,{end_start_formatted}.00,{total_time_formatted}.00,Default,,0,0,0,,{{\\an1\\fad(500,500)}}{subtitle}\n')
        logger.info('Subtitle file created successfully')
        return subtitle_path
    except Exception as e:
        logger.error('Failed to create subtitle file: {}', e)
        return False

def format_duration(seconds, trim=False):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if trim:
        if hours > 0:
            return '{}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
        elif minutes > 0:
            return '{}:{:02}'.format(int(minutes), int(seconds))
        else:
            return '00:{:02}'.format(int(seconds))
    else:
        return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
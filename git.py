import logging
import subprocess
import sys

from semantic_version import Version
from util import colargulog, constants

logger = logging.getLogger(__name__)

DEBUG = False

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

logger.info('Updating The Music Video Downloader on Github')

curVersion = Version(constants.VERSION)

nextPatchVersion = Version(constants.VERSION)
nextPatchVersion.patch += 1
nextMinorVersion = Version(constants.VERSION)
nextMinorVersion.minor += 1
nextMinorVersion.patch = 0
nextMajorVersion = Version(constants.VERSION)
nextMajorVersion.major += 1
nextMajorVersion.minor = 0
nextMajorVersion.patch = 0

logger.info('The current version number is {}', curVersion)
logger.info('   1) Major version: {}', nextMajorVersion)
logger.info('   2) Minor version: {}', nextMinorVersion)
logger.info('   3) Patch version: {}', nextPatchVersion)
while True:
    logger.info('----')
    logger.info('Select the corresponding number next to the next desired version.')
    user_input = input('[>>>>] - ')
    try:
        value = int(user_input)
        if value >= 1 and value <= 3:
            if value==1:
                nextVersion = nextMajorVersion
            elif value==2:
                nextVersion = nextMinorVersion
            else:
                nextVersion = nextPatchVersion
            logger.info('You have selected {} as the next version.', nextVersion)
            logger.info('Confirm (Y/N)?')
            if input('[>>>>] - ').lower() == 'y':
                break
        else:
            logger.error('Invalid input, please enter a number between 1 and 3.')
    except ValueError:
        logger.error('Invalid input, please enter a number between 1 and 3.')
logger.info('Version {} Configmred', nextVersion)

logger.debug('Updating version in {}...', 'util/contsants.py')
with open('util/constants.py', 'r') as file:
    content = file.readlines()

for i, line in enumerate(content):
    if line.casefold().startswith('version'):
        content[i] = f"VERSION = '{nextVersion}'\n"

with open('util/constants.py', 'w') as file:
    file.writelines(content)
logger.debug('Successfully updated version in {}.', 'util/contsants.py')

# Git Update
logger.info('Would you like to commit changes to git (Y/n)?')
if input('[>>>>] - ').lower() == 'n':
    sys.exit()

logger.info('Enter a description for this commit.')
m = input('[>>>>] - ')
m = f'V{nextVersion}: {m}'

# Add
add_command = ['git', 'add', '.']
add_result = subprocess.run(add_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
if add_result.returncode == 0:
    logger.info(add_result.stdout)
else:
    logger.error(add_result.stderr)
    sys.exit()

# Commit
commit_command = ['git', 'commit', '-m', m]
commit_result = subprocess.run(commit_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
if commit_result.returncode == 0:
    logger.info(commit_result.stdout)
else:
    logger.error(commit_result.stderr)
    sys.exit()

# Push
push_command = ['git', 'push', 'origin', 'main']
push_result = subprocess.run(push_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
if push_result.returncode == 0:
    logger.info(push_result.stdout)
    logger.info('Successfully updated project to git.')
    sys.exit()
else:
    logger.error(push_result.stderr)
    sys.exit()
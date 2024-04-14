<h2 align="center">MVD (Music Video Downloader)</h2>
<p align="center">A simply python script that downloads Music Videos from the web and organizes them into a directory. Also includes a basic player script as well.</p>
<div align="center">
  
  ![GitHub documentation](https://img.shields.io/badge/documentation-yes-brightgreen.svg?style=flat-square)
  ![GitHub repo size](https://img.shields.io/github/repo-size/chrisjameschamp/mvd?style=flat-square)
  ![Github repo languages](https://img.shields.io/github/languages/count/chrisjameschamp/mvd?style=flat-square)
  ![Github repo top lang](https://img.shields.io/github/languages/top/chrisjameschamp/mvd?style=flat-square)
  ![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/chrisjameschamp/mvd)
  ![GitHub license](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)
  ![GitHub last commit](https://img.shields.io/github/last-commit/chrisjameschamp/mvd?style=flat-square)

</div>
## Index

* [Music Video Downloader](#mvd)
* [Download](#download)
* [Install](#install)
  * [Dependencies](#dependencies)
  * [Automated Install](#automated-install)
  * [Manual Install](#manual-install)
* [Running MVD](#running-mvd)
  * [Searching](#searching)
  * [Manual Importation](#manual-importation)

## Download

To download the project simply pull the project down using git commands
```sh
git clone https://github.com/chrisjameschamp/mvd.git
```

## Install

Once the project has been download navigate to the mvd folder.
```sh
cd mvd
```

### Dependencies

The project requires atleast Python 3.11.

In order to automate the install you must have pipenv installed on your system.

### Automated Install

Once you have python and pipenv installed you can install all the dependencies and setup the python environment by running the install script
```sh
./install.sh
```

This script will create a virtual environment for the project and install dependencies.

### Manual Install

You can also install the dependencies manually.  The list of dependencies are listed below.

* Colorama
* Yt-dlp
* Tqdm

If you choose to install mvd manually you will need to directly run the mvd.py file and not the mvd.sh file as the shell file is designed to run on the virutal environment instead of the installed python version.

```sh
./mvd.py
```

## Running MVD

After you have installed MVD you can simply run it with the mvd.sh script.

```sh
./mvd.sh
```

If you installed MVD manually without the installation script then you would need to run the python script directly instead of the shell script.

If everything is running correctly you should be greeted by a similar message:

```sh
[INFO] - Welcome to Music Video Downloader
[INFO] -    1) Search the Internet Music Video Database
[INFO] -    2) Manually Add Youtube Video
[INFO] -    3) Exit
[INFO] - Select a value 1-3
```

### Searching

You can search the Internet Music Video Database for music vidoes and get their youtube video for downloading automagically.

By default it will search for each word as a seperate search.  For example a search query of Ringo Star will search for Ringo and Star seperatly and may result in more results than desired.

You can search for a specific phrase by surrounding the search query in quotes.  For example a search query of "Ringo Star" will only search for entries with exactly "Ringo Star" as the artist or title.

Keep in mind when using the Internet Music Video Database, not all videos are listed and you may need to manually add the video via the Youtube url if the Internet Music Video Database cannot find what you are looking for.  Also some videos have outdated information and are no longer available at the code on file, and/or the video may be set to private in which we will not be able to download those.

Videos using vimeo will be skipped for now, however vimeo support is coming.

### Manual Importation

Documenation Coming soon but it's pretty straight forward.

## 
<div align="center">
  <a href="https://paypal.me/Champeau?country.x=US&locale.x=en_US"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black"></a>
</div>
# Spotify-Playlist-Downloader
Downloads all the songs in a Spotify Playlist and stores them locally.


This Python script works by first scraping the links to each song from the Spotify Playlist web page and visiting each link individually to extract the title which contains the song's name.
The script then takes each name and the artist who created the song and searches it on YouTube.
Then it takes the first search result, downloads only the audio, and stores it in the "downloaded_songs" folder.

Run using "python3 download-music.py"

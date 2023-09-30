#!/bin/python3

import requests
from bs4 import BeautifulSoup
import os
import re
import sys
import time
import pytube



try:
	def get_playlist():
		while True:
			try:
				playlist = str(input("Enter link to Spotify Playlist: "))

				#input validation
				playlist_split = str(playlist).split("/")
				if str(playlist_split[2]).lower() == "open.spotify.com" and str(playlist_split[3]).lower() == "playlist":
					break
				else:
					playlist = input("Enter link to Spotify Playlist: ")
			except:
				playlist = str(input("Enter link to Spotify Playlist: "))

		return playlist
		


	def get_soup(URL):
		#get HTML(soup element)
		response = requests.get(url)
		html = response.text
		soup = BeautifulSoup(html, "html.parser")
		
		return soup



	def create_song_link_list(soup):
		song_link_list = []
		#extract all <meta> elements
		for song in soup.find_all("meta"):
			#exctect content, which contains link to each song from <meta> elements
			content = str(song.get("content"))
			content_split = content.split("/")
			try:
				if str(content_split[2]).lower() == "open.spotify.com" and str(content_split[3]).lower() == "track":
					song_link_list.append(content)
			except:
				pass

		return song_link_list



	def create_song_list(song_link_list):
		song_list = []
		#visit each song link individually and extract the page title which contains the song name and author
		for song in song_link_list:
			song_link = str(song)
			soup = get_soup(song_link)
			
			while True:
				try:
					page_title = str(soup.title.text.strip())
					break
				except AttributeError:
					soup = get_soup(song_link)

			page_title_split = page_title.split("|")
			
			song_list.append(page_title_split[0])
		
		return song_list



	def get_video_links(song_list):
		vid_links = []
		#search for each song on youtube
		for song in song_list:
			search_query = str(song).split()
			search_query = "+".join(search_query)

			soup = get_soup(f"https://www.youtube.com/results?search_query={search_query}")

			contents = str(soup.prettify())

			accepts = 0

			lines = contents.split(":")
			search_term = re.compile(r"\bwatch\?v\=")
			comparison = re.compile(r"\w\\\w\w")
			#go through the HTML for the search results and extract the watch code for each video
			while accepts < 16:
				for line in lines:
					if search_term.search(line) != None:
						line = line.split(",")
						if len(line[1]) < 20:
							line_check = str(line[0]).split("\\")
							if len(str(line_check[1])) <= 100:
								vid_links.append(str(line[0]))
								accepts += 1
								print(f"\nVideo link for: {song} has been extracted.")
								time.sleep(3)
								while_break = True
								break
							else:
								soup = get_soup(f"https://www.youtube.com/results?search_query={search_query}")
								contents = str(soup.prettify())
								lines = contents.split(":")
								print(f"\nError while extracting video link for: {song}.")
								print("Reiterating until successful.")
								time.sleep(1)
				if while_break == True:
					break
		
		return vid_links



	def run_main():
		playlist = get_playlist()
		print("\nPlaylist has been validated.")
		print("Proceeding to extracting song names.")
		time.sleep(3)

		soup = get_soup(playlist)

		song_link_list = create_song_link_list(soup)
		
		song_list = create_song_list(song_link_list)
		print("\nSong names have beeen extracted.")
		print("Proceediding with searching for songs on YouTube")
		time.sleep(3)

		vid_links = get_video_links(song_list)
		print("\nVideo links have been successfully extracted.")
		print("Proceeding with response checks.\n")
		time.sleep(3)


		accepts = 0
		#checking connection with youtube video
		for link in vid_links:
			while accepts < 16:
				url = f"https://youtube.com{str(link).strip()}"
				url_split = url.split("\"")
				formatted_url = "".join(url_split)
				print(formatted_url)

				response = requests.get(formatted_url)
				print(f"{response}\n")

				if str(response) == "<Response [200]>":
					accepts += 1
					break
				else:
					print("Reiterating until response check is successful.")

		print("\nResponse checks were successful.")
		print("Proceeding with audio stream download.")



		#creating a directory for the downloaded songs
		try:
			os.mkdir("downloaded_songs")
		except FileExistsError:
			pass

		song = 0
		#download songs
		for link in vid_links:
			while True:
				try:
					yt = pytube.YouTube(str(link))

					stream = yt.streams.filter(only_audio=True)
					stream_split = str(stream).split("\"")

					itag = stream_split[1]

					print("\n")
					print("-" * 50)
					print(f"Downloading audio stream for {song_list[song]}")
					audio_stream = yt.streams.get_by_itag(itag)
					try:
						audio_stream.download("downloaded_songs")
					except PermissionError:
						print("Lacking permissions to download in designated directory.")
						print("Attempting to download in current directory.")
						
						audio_stream.download()
					print("Download complete")
					print("-" * 50)

					song += 1
					break
				except AttributeError:
					pass





	run_main()


	
except KeyboardInterrupt:
	print("\nExiting Program")
	sys.exit()

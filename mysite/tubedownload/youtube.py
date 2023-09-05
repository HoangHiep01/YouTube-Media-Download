import json
import os

from pytube import YouTube
from threading import Thread

class DownloadMedia():

	def __init__(self, link):
		self.link = link
		self.youtube = YouTube(link)
		self.videos = None
		self.audios = None

	def list_video_option(self):
		list_options_video = self.youtube.streams.filter(type='video').order_by('resolution').asc()

		result = dict()

		for idx, option in enumerate(list_options_video):
			result[f'option_{idx}'] = {
				'itag': option.itag,
				'resolution': option.resolution,
				'fps': option.fps,
				'type': option.mime_type,
				'video_codec': option.video_codec,
				'audio_codec': option.audio_codec,
			}
			if result[f'option_{idx}']['audio_codec'] is None:
				result[f'option_{idx}']['audio_codec'] = "Video without sound."
			# print(type(result[f'option_{idx}']['audio_codec']), result[f'option_{idx}']['audio_codec'])

		self.videos = result
		return result

	def list_audio_option(self):
		list_options_audio = self.youtube.streams.filter(type='audio').order_by('bitrate').asc()

		result = dict()

		for idx, option in enumerate(list_options_audio):
			result[f'option_{idx}'] = {
				'itag': option.itag,
				'type': option.mime_type,
				'audio_codec': option.audio_codec,
				'avg_bitrate': option.abr,
			}

		self.audios = result
		return result

	def list_media_option(self):

		# video_thread = Thread(target=self.list_video_option)
		# audio_thread = Thread(target=self.list_audio_option)

		# video_thread.start()
		# audio_thread.start()

		# video_thread.join()
		# audio_thread.join()
		
		self.list_audio_option()
		self.list_video_option()

		assert self.videos is not None and self.audios is not None, "Audio or Video is None or both."
		return {'video' : self.videos, 'audio' :  self.audios}


	def download(self, itag=None, custom_path="/tubedownload/static/media/"):

		assert itag is not None, "itag required"
		path = os.getcwd() + custom_path
		media = self.youtube.streams.get_by_itag(int(itag))

		output_file = media.download(output_path=path + f'{media.type}/')
		# print(output_file)

		# base, ext = os.path.splitext(output_file)
		# new_file = base + set_ext
		# os.rename(output_file, new_file)
		with open(output_file, 'rb') as file:
			content = file.read()

		os.remove(output_file)
		return {'file': content, 'title': media.title, 'ext': media.subtype, 'type': media.type}


if __name__ == '__main__':

	example = DownloadMedia("https://www.youtube.com/watch?v=95ahbau-rJk")
	# print(json.dumps(example.list_video_option()))
	# print()
	# print(json.dumps(example.list_audio_option()))
	print(json.dumps(example.list_media_option(), indent=4))
	# itag = int(input("Itag: "))
	# print(example.download(itag)['title'])
	example.download(itag=17)
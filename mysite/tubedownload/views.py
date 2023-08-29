from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from pytube import YouTube
from .youtube import DownloadMedia

import os
import json

# Create your views here.

def home(request):

	if request.method == "GET":
		return render(request, "tube/home.html", {})

	if request.method == "POST":
		link = request.POST['youTube-link']
		media = DownloadMedia(link)
		option = media.list_media_option()
		context = {
			'link' : link,
			'videos' : media.videos,
			'audios' : media.audios,
			'media_title': media.youtube.title,
			'thumbnail': media.youtube.thumbnail_url,
		}
		# print(json.dumps(option, indent=4))
		return render(request, "tube/choose.html", context)

def download(request):

	if request.method == "POST":
		path = os.getcwd() + "/tubedownload/static/media/"
		link = request.POST['link']
		media_type = request.POST['flexRadioDefault']
		itag = int(request.POST['flexRadioItems'])
		yt = YouTube(link)
		stream = yt.streams.get_by_itag(itag)
		if media_type == 'mp3':
			output_file = stream.download(output_path=path+'audio/')
			base, ext = os.path.splitext(output_file)
			new_file = base + '.mp3'
			os.rename(output_file, new_file)
			file = open(new_file, 'rb')
			# response = FileResponse(file)
			response = HttpResponse(
				file,
				headers={
				"Content-Type": "audio/mpeg",
				"Content-Disposition": f'attachment; filename="{yt.title}.mp3"',
				},
			)
			os.remove(new_file)
		elif media_type == 'mp4':
			output_file = stream.download(output_path=path+'video/')
			base, ext = os.path.splitext(output_file)
			new_file = base + '.mp4'
			os.rename(output_file, new_file)
			file = open(new_file, 'rb')
			# response = FileResponse(file)
			response = HttpResponse(
				file,
				headers={
				"Content-Type": "video/mp4",
				"Content-Disposition": f'attachment; filename="{yt.title}.mp4"',
				},
			)
			os.remove(new_file)

	return response
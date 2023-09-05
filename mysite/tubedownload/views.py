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
		# path = os.getcwd() + "/tubedownload/static/media/"
		link = request.POST['link']
		itag = int(request.POST['itag'])
		media = DownloadMedia(link)
		result = media.download(itag=itag)

		file_name = result['title']
		extension = result['ext']

		if result['type'] == 'video':
			response = HttpResponse(
					result['file'],
					headers={
					"Content-Type": "video/mp4",
					"Content-Disposition": f'attachment; filename="{file_name}.{extension}"',
					},
				)
		elif result['type'] == 'audio':
			response = HttpResponse(
					result['file'],
					headers={
					"Content-Type": "audio/mpeg",
					"Content-Disposition": f'attachment; filename="{file_name}.{extension}"',
					},
				)
	return response
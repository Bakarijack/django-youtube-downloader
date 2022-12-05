from django.shortcuts import render, redirect
from pytube import *
from django.views.generic import View
import os
# Create your views here.

class Home(View):
    def __init__(self, url = None):
        self.url = url
        
    def get(self, request):
        return render(request, 'app/home.html')
    
    def post(self, request):
        #for fetching videos
        if request.POST.get('fetch-vid'):
            self.url = request.POST.get('given-url')
            video = YouTube(self.url)
            vidTitle,vidThumbnail = video.title,video.thumbnail_url
            qual,stream = [],[]
            
            for vid in video.streams.filter(progressive=True):
                qual.append(vid.resolution)
                stream.append(vid)
            
            context = {'vidTitle':vidTitle,'vidThumbnail':vidThumbnail,'qual':qual,'stream':stream,'url':self.url}
            
            return render(request, 'app/home.html', context)
        elif request.POST.get('download-vid'):
            self.url = request.POST.get('given-url')
            video = YouTube(self.url)
            stream = [x for x in video.streams.filter(progressive=True)]
            chosen_qual = video.streams[int(request.POST.get('download-vid')) - 1 ]
            
            #getting the Download path
            if os.name == 'nt':
                DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"
            else: #PORT: FOR * Nix Systems
                DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads"
            #chosen_qual.download(output_path = '../../Downloads')
            chosen_qual.download(DOWNLOAD_FOLDER)
            
            return redirect('home')
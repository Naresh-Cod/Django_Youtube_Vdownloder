from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from pytube import YouTube
import os
import re


# Create your views here.

def welcome(request):
    return render(request, 'main_doc.html')



def is_valid_youtube_url(url):
    # Regular expression to validate YouTube URLs
    # This is a simple example, and you may want to use a more comprehensive regex
    return re.match(r'^https?://(?:www\.)?youtube\.com/watch\?v=\w+', url)

def show_cli_b(request):
    global url
    url = request.GET.get('link')
    #print(url)

    if not url or not is_valid_youtube_url(url):
        error = render(request, 'error.html')
        return HttpResponse(error)
        # return HttpResponse("Invalid or missing YouTube video link.")

    try:
        obj = YouTube(url)

        '''video = obj.streams.filter(progressive=True).all()
        for i in video:
            print(i)'''

        lis = []
        video_resolutions = obj.streams.all()
        #print(video_resolutions)
        for i in video_resolutions:
            lis.append(i.resolution)
        # =======================================================
        # Filter out None values and create a list of resolutions
        resolutions = [res for res in lis if res is not None]
        unique_resolutions = list(set(resolutions))

        # Create a dictionary to map the string resolutions to corresponding numerical values
        resolution_values = {'144p': 144, '240p': 240, '360p': 360,
                              '480p': 480, '720p': 720, '1080p': 1080, '1440p': 1440, '2160p': 2160,}

        # Sort the resolutions in descending order based on their numerical values
        sorted_resolutions = sorted(unique_resolutions, key=lambda x: resolution_values[x], reverse=True)

        # =======================================================

        # -------------------------------------
        link = url.replace("watch?v=", "embed/")        
        try:
            yt = YouTube(link)
            vid_thub = yt.thumbnail_url
            #video_stream = yt.streams.get_highest_resolution()
            #video_url = video_stream.url
        except Exception as e:
            # Handle any errors that might occur during fetching the video URL
            video_url = None
        # ----------------------------------------

        title = obj.title
        time = obj.length
        channel_id = obj.author

        text = {'vid_thub': vid_thub, 'title': title, 'time': time, 'channel_id': channel_id, 'video_res': sorted_resolutions}

        return render(request, 'click_dow.html', text)
    
    except Exception as e:
        # Handle any exceptions that might occur during the process
        return HttpResponse("Error occurred while fetching YouTube video details: " + str(e))



def done_dow_ur(request, resolution):
    obj = YouTube(url)
    homedir = os.path.expanduser('~')
    dirs = homedir + '/Downloads'
    #print('dirs = ', dirs)

    if request.method == "POST":
        #selected_stream = obj.streams.get_by_resolution(resolution)
        selected_stream = obj.streams.filter(res=resolution).first()

        if selected_stream:
            try:
                selected_stream.download(dirs)
                return render(request, 'download_complete.html')
            except Exception as e:
                return render(request, 'download_error.html', {'error_message': str(e)})
        else:
            return render(request, 'download_error.html', {'error_message': 'Selected resolution is not available for this video.'})
    else:
        return render(request, 'download_error.html', {'error_message': 'Invalid request method.'})


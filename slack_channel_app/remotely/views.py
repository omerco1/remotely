from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import Channel

# Create your views here.
def index(request):
    #return HttpResponse("Hello!") 

    #ordering objects from model by date: 
    #objs = MyModel.objects.all().order_by("-date")

    # appending new row to db: 
    # m3 = MyModel(my_id=2, date=today, title='hello')
    # m3.save() 

    context = { 
        'channels': Channel.objects.all(),
        'omer': 'asdfasdfasdfasdflkasdjf'
    }
    return render(request, "index.html", context)

def fetch_channel(request, channel_name): 
    channel = ''
    try: 
        channel = Channel.objects.get(name=channel_name)
    except Channel.DoesNotExist: 
        raise Http404("Channel does not exist :(")
    
    context = {'channel_name': channel }

    return render(request, "channel.html", context)
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *
import uuid
import datetime

# when inheriting from a super in python to overwrite constructor
# super().__init__(fname, lname)

# Getting currently registered user: 
# author = models.ForeignKey(get_user_model())

# Create your views here.
@login_required(login_url='login/')
def index(request):

    if not request.user.is_authenticated:
        return render(request, "login.html")

    current_user = (User.objects.get(username=request.user.username))    
    try: 
        channel_member_obj = Channel_Member.objects.get(user=current_user)
        users_channel_feed = channel_member_obj.channels.all()
    except: 
        users_channel_feed = [] 
        channel_member_obj = None 
    
    # if user has no channels indicate no channels 
    if len(users_channel_feed) ==0 : 
        create_channel_msg = 'You have no channels, browse around and join one you like!'
    else: 
        create_channel_msg = '' 
    # For now pulling all users available as a proof of concept
    users = Channel_Member.objects.all()
    context = { 
        'channels': users_channel_feed,
        'username': request.user,
        'users' : users,
        'message': create_channel_msg

    }
    # Creating new channel 
    if request.method == 'POST':
        try: 
            if Channel.objects.get(name=request.POST['channel_name']): 
                context["message"] = 'Error: Channel with that name already exists!'
                return render(request, "index.html", context) 
        except: 
            is_public = False
            try: 
                is_public = True if ((request.POST['private_channel_check']) == 'on') else False 
            except: 
                print('here')
                is_public = False
            
            print(is_public)
            chan = Channel(name=request.POST['channel_name'], num_users=1, public=is_public)
            chan.save()
            
            chanMem = Channel_Member()
            chanMem.user = current_user
            chanMem.channels.add(chan)
            chanMem.save()
            
            # TODO: Change to query by uuid
            #chanMem.user =   # get_user_model()
            #print(f"user: {User.objects.get(username=request.user.username).username} uuid: {User.objects.get(username=request.user.username).uuid}")
            #chanMem.channels = chan 
            #chanMem.save()
            
        
    #return HttpResponse("Hello!") 

    #ordering objects from model by date: 
    #objs = MyModel.objects.all().order_by("-date")

    # appending new row to db: 
    # m3 = MyModel(my_id=2, date=today, title='hello')
    # m3.save() 

    #seeing sql command from migrations defined: 
    # python3 manage.py sqlmigrate remotely 0001

    return render(request, "index.html", context)

# @login_required(login_url='login/')
def fetch_channel(request, channel_name): 
    if not request.user.is_authenticated:
        return render(request, "login.html")

    channel = ''
    try: 
        channel = Channel.objects.get(name=channel_name)
    except ObjectDoesNotExist: 
        raise Http404("Channel does not exist :(")
    
    context = {
        'channel_name': channel,
        'members': channel.members.all()
    }

    return render(request, "channel.html", context)

def login_view(request):

    try: 
        if request.method == 'POST':
            usern = request.POST['username']
            passw = request.POST['password']
            user = authenticate(request, username=usern, password=passw)
            if user is not None: 
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else: 
                return render(request, 'login.html', {'message': 'Invalid credentials'})
    except: 
        print('POST failed.')

    return render(request, "login.html", {'message': None})


#TODO: Modift LOGIN_URL in settings.py
def logout_view(request): 
    logout(request)
    print('DBG: Logging out !')
    #return HttpResponseRedirect(reverse('login'))
    return render(request, 'login.html', {'message': None})

def search(request): 
    return render(request, 'search.html')

def reqister_user(request): 

    try: 
        email = request.POST['email']
        first_name= request.POST['first']
        last_name = request.POST['last']
        username = request.POST['username']
        password = request.POST['password']
        conf_pass = request.POST['conf_password']

        user = authenticate(request, username=username, password=password)
        if user is not None: 
            return render(request, 'login.html', {'message': 'There is an account already registered with those credentials try again'})
        user = User.objects.create_user(username, email, password)
        if user is not None: 
            user.first_name = first_name
            user.last_name = last_name
            user.uuid = uuid.uuid1()
            user.date_joined = datetime.datetime.now()
            user.save()
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
       print('POST failed.' + str(e))

    return render(request, "register.html", {'message': None})


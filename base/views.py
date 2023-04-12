from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from .models import Room, Topic, Message
from django.db.models import Q
from .forms import RoomForm, TopicForm

# Create your views here.

def loginPage(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    # if the user is logged in oneself can't go to login page

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get('username=username')
        except:
            pass
            # messages.error(request, 'User does not exists')
            # now go to main.html and type 
            # upto this code you will get 'User does..' even if user exists
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User or Password is Wrong')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')



def registerPage(request):
    # page = 'register'
    # no need the above line
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            # username = request.POST.get('username').lower()
            # as the username is only taken in lowercase
            user.save ()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An Error Occured')
   
    return render(request, 'base/login_register.html', {'form': form})


# after creating each difination go to urls.py
#  to define path
def test(request):
    return HttpResponse('"bon jour" by TANAY and it is in base/views.py ')

# @login_required(login_url='login')
# If you want that user must be logged in to view home page
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''# remember in home browse topic 
    # we have <a href="{% url 'home' %}?q={topic.name}}">
    # rooms = Room.objects.all() # For all objects
    # also if else for getting the request
    # instead of q if we use any other it won't func well as 
    # <a href="{% url 'home' %}?q={topic.name}}">
    # 
    # now the search option is in nabar.html
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | #for the school name
        Q(name__icontains=q) |
        # Q(description__icontains=q) |
        Q(recoTest__icontains=q) |
        # Q(recoUniv__icontains=q) |
        Q(recoUniv__icontains=q) 
        ) # topic__name__"icontains"=q for all show
    # import Q for querry then querry__iscontains=q for search
    # as we want 'and' 'or' options in search
    # As in models.py Class Room we have topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    topic_count = topics.count() # <h5>{{room_count}} rooms available</h5>
    # in the home.html now create library in context
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count, 
               'topic_count': topic_count,
               'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
     # Check if logged-in user is the host
    # Check if logged-in user is the host or a superuser
    if request.user != room.host and not request.user.is_superuser and not request.user.is_staff:
        return redirect('home')

    # class Meta:
        # For Ascending order
        # ordering = ['-updated', '-created']
        # if it is in models.py in class Messages
    room_messages = room.message_set.all()
    # room_messages = room.message_set.all().order_by('-created')
    # we can query the child object from specific object in models
    # here. In this case we have model name Message in models.py.
    # but here room.message_set in this command put the first letter
    # in lower case. This above rel is many to one
    counsellors = room.counsellors.all()
    # This above method is for many to many relation
    if request.method == 'POST':
        # we are using the model form which going to autogenerate
        # we are using create method here we can also do update 
        # method or save method. so now go to models.py to see objects
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
            # here 'body' passed from the body we get from room.html

        ) 
        room.counsellors.add(request.user)
        # to add user automatically
        return redirect('room', pk=room.id)   
    # technically this above redirect is not required but if we don't do it then it can mess up with some other functions technically so it is better to do that.

    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i

    # context = {'room': room }
    context = {
        # 'room': room,
        'room_name': room.name,
        'room_host': room.host,
        'room_topic': room.topic,
        'room_class': room.Class,
        'room_description': room.description,
        'room_messages': room_messages,
        'counsellors': counsellors,
        'room_India_Abroad': room.India_Abroad,
        'room_summary': room.summary,
        'room_recoTest': room.recoTest,
        'room_recoUniv': room.recoUniv,
        'room_subjects': room.subjects,
        'room_dreamCareer': room.dreamCareer,
        'room_majorPlan': room.majorPlan,
        'room_emailID': room.emailID,
        'room_contactID': room.contactID,
        # 'room_capacity': room.capacity,
        # Add any other fields you want to display here
    }

    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


def createTopic(request):
    form = TopicForm()

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/topic_form.html', context)

@login_required(login_url='login')
# @user_passes_test(lambda u: u.is_superuser, login_url='home')
# import the following two packages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
def createRoom(request):

    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    
    form = RoomForm()

    if request.method == 'POST':
        # request.POST.get('name')
        form = RoomForm(request.POST)
        if form.is_valid():
            # to automatically submit the host; write the following to lines
            # room = form.save(commit=False)
            # room.host = request.user
            form.save()
            return redirect('home')
        # import redirect from django.shortcuts
        # cause I have name = "home" in urls.py
    # now create a blank dictionary entry as context
    context ={'form': form}
    # Now we have a form and have post that data 
    # add the form in the data
    # check the validity and save
    # and then we direct it to the data base
    # and create new room
    # check room_form.html
    return render(request, 'base/room_from.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):

    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)


    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home') # replace 'home' with the name of your room list view


    context ={'form':form}
    
    return render(request, 'base/room_from.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if not request.user.is_superuser: #request.user != room.host:
        # if request.user != room.host: or request.user....
        # if the user is not the host of the room, redirect to an error page or show a message
        messages.error(request, 'You are not authorized to delete this room')
        return redirect('home')
    # visible with differe host

    if request.method == 'POST':
        room.delete()
        return redirect('home') # replace 'home' with the name of your room list view
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user: #or not request.user.is_superuser :
        # message has a owner which is defines as user in models.py
        # in Message object
        messages.error(request, 'You are not authorized to delete this room')
        return redirect('home')
    # visible with differe host

    if request.method == 'POST':
        message.delete()
        return redirect('home') # replace 'home' with the name of your room list view
    return render(request, 'base/delete.html', {'obj': message.body})

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
import csv

# @login_required(login_url='login')
def export_rooms_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rooms.csv"'

    # Create a csv writer object
    writer = csv.writer(response)

    # Write column headers
    writer.writerow(['Name', 'Description', 'Topic', 'Class', 'Host'])

    # Get data from Room model
    rooms = Room.objects.all().values_list('name', 'description', 'topic__name', 'Class__name', 'host__username')

    # Write data rows to csv
    for row in rooms:
        writer.writerow(row)

    return response
###########################################################################################
###########################################################################################
###########################################################################################

    

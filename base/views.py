from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages # for login error message
from django.contrib.auth.decorators import login_required # for login-user permision
from django.db.models import Q # for multiple search
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm # for register
# import User-defined classes
from .models import Room, Topic, Message, User # in base/model.py
from .forms import RoomForm, UserForm, MyUserCreationForm # Customize Register Form

# The order doesn't matter

def loginPage(request):
	page = 'login'

	if request.user.is_authenticated: # forbid login again
		return redirect('home')

	if request.method == "POST":
		email = request.POST.get('email').lower() # get by name
		password = request.POST.get('password')
		try:
			user = User.objects.get(email = email)
		except:
			messages.error(request, 'User does not exist')
		
		user = authenticate(request, email = email, password = password)

		if user:
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, 'Username OR password does not exist')

	context = {'page': page}
	return render(request, 'base/login_register.html', context)

def logoutUser(request):
	context = {}
	logout(request)
	return redirect('home')

def registerPage(request):
	form = MyUserCreationForm(request.POST)

	if form.is_valid(): # check if the form is valid
		form = MyUserCreationForm(request.POST)
		user = form.save(commit=False)
		user.username = user.username.lower() # lower case
		user.save()
		login(request, user)
		return redirect('home')
	else:
		messages.error(request, 'An error has occurred during registration')
	context = {'form': form}
	return render(request, 'base/login_register.html', context)


def home(request):
	'''
	Index Home Page
	request: HttpRequest object
	'''
	q = request.GET.get('q') if request.GET.get('q') else ''

	# Search multiple domains meanwhile
	rooms = Room.objects.filter(
		Q(topic__name__icontains = q) |
		Q(name__icontains = q) |
		Q(description__icontains = q)
		) # '__icontains' means partial matching

	topics = Topic.objects.all()[:5] # get the topic (id == 1)

	room_count = rooms.count()

	# display all the messages related to the room's topic
	room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
	
	context = {'rooms': rooms, 
				'topics': topics, 
				'room_count': room_count, 
				'room_messages': room_messages}
	return render(request, 'base/home.html', context)

def room(request, pk):
	room = Room.objects.get(id=pk) # get the room (id == pk)
	
	# get all the messages in the room by descending created-time 
	room_messages = room.message_set.all().order_by('-created') # _set: many to one relationship

	participants = room.participants.all() # many to many relationship
	
	if request.method == 'POST':
		message = Message.objects.create(
			user = request.user,
			room = room,
			body = request.POST.get('body')
		)
		room.participants.add(request.user)
		return redirect('room', pk=room.id)

	context = {	'room':room, 
				'room_messages': room_messages, 
				'participants': participants} # pass to Template
	return render(request, 'base/room.html', context)

def userProfile(request, pk):
	user = User.objects.get(id = pk)
	rooms = user.room_set.all() # _set: get all
	room_messages = user.message_set.all()
	topics = Topic.objects.all()

	context = {	'user': user, 
				'rooms': rooms,
				'room_messages':room_messages, 
				'topics': topics}
	return render(request, 'base/profile.html', context)

# Decorator 使用该函数时必须登录
@login_required(login_url='login') # login required when create
def createRoom(request):
	form = RoomForm()
	topics = Topic.objects.all()
	if request.method == 'POST':
		topic_name = request.POST.get('topic')
		topic, created = Topic.objects.get_or_create(name = topic_name)
		# Room(models.Model)的父类内置方法
		Room.objects.create(
			host = request.user,
			topic = topic,
			name = request.POST.get('name'),
			description = request.POST.get('description')
		)
		return redirect('home') # namespace of the url
		
	context = {'form': form, 'topics': topics}
	return render(request, 'base/room_form.html', context)

@login_required(login_url='login') # login required when update
def updateRoom(request, pk):
	room = Room.objects.get(id=pk)
	form = RoomForm(instance=room) # instantiate
	topics = Topic.objects.all()
	if request.user != room.host:
		return HttpResponse('You are not allowed here!!')

	if request.method == 'POST':
		topic_name = request.POST.get('topic')
		topic, created = Topic.objects.get_or_create(name = topic_name)
		room.name = request.POST.get('name')
		room.topic = topic
		room.description = request.POST.get('description')
		room.save()
		return redirect('home')	

	context = {'form': form, 'topics': topics, 'room': room}
	return render(request, 'base/room_form.html', context)	

@login_required(login_url='login') # login required when delete
def deleteRoom(request, pk):
	room = Room.objects.get(id=pk)

	if request.user != room.host:
		return HttpResponse('You are not allowed here!!')
	if request.method == 'POST':
		room.delete()
		return redirect('home')
	return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login') # login required when delete
def deleteMessage(request, pk):
	message = Message.objects.get(id=pk)

	if request.user != message.user:
		return HttpResponse('You are not allowed here!!')
	if request.method == 'POST':
		message.delete()
		return redirect('room', pk=message.room.id) # redirect to the formal room
	return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q) # 包含关键词q
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
	# Get and Deliver [All Messages] to 'activity.html'
    room_messages = Message.objects.all() 
	# 'activity.html' can use 'room_messages' in {% for _ in room_messages %}
    return render(request, 'base/activity.html', {'room_messages': room_messages})
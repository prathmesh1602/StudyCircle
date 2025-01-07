from django.shortcuts import render,redirect
from .models import Room,Topic
from django.db.models import Q
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username) 
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username Or Password Does NOt exist')



        
    context={}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')











def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) 
                                |Q(name__icontains=q) 
                                |Q(description__icontains=q)
                                )# to get filterd objects with topic name provided form Room 
    
    
    room_cont = rooms.count()
    topic = Topic.objects.all()# to get all entity from topic

    context = {'rooms':rooms,'topics':topic,'room_count':room_cont}
    return render(request,'base/home.html',context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    
    context = {'room':room}        
    return render(request,'base/room.html',context)

@login_required(login_url='login')
def creatroom(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateroom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        form = RoomForm(request.POST,instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteroom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})



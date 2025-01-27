from django.shortcuts import render,redirect
from .models import Room,Topic,Message,User
from django.db.models import Q
from .forms import RoomForm,CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import UserDetails
from .forms import UserDetailsForm
def loginPage(request):
    page='page'
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username)
        print(password)
        try:
            user = User.objects.get(username=username) 

        except:
            messages.error(request,'User does not exist')

        user = authenticate(request,username=username,password=password)
        

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username Or Password Does Not exist')



        
    context={'page':page}
    return render(request,'base/login.html',context)


def registeruser(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form =CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            print(form)
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(error)
                    messages.error(request, f"{field.capitalize()}: {error}")
           
 
    return render(request,'base/register.html', {'form': form})

def resetpassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1:
            messages.error(request, "All fields are required.")
            return render(request, 'base/reset_password.html')
        if password1 != password2:
            messages.error(request, "Password not Matching")
        else:
            try:
                user = User.objects.get(username=username)
                user.set_password(password1)
                user.save() 
                messages.success(request, "Password reset successfully!")
                return redirect('login')  
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")


        

    return render(request, 'base/reset_password.html')





def logoutUser(request):
    logout(request)
    return redirect('home')

def userprofile(request,pk):
    user = User.objects.get(id=pk)
    user_details = UserDetails.objects.get(user=request.user)
    rooms = user.room_set.all()
    room_messages =user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics,'user_details': user_details}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def updateuser(request):
    user = request.user
    user_details, created = UserDetails.objects.get_or_create(user=request.user)
    user_form = CustomUserCreationForm(instance=user)
    details_form = UserDetailsForm(instance=user_details)
    context = {
        'user_form': user_form,
        'details_form': details_form
    }

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, request.FILES, instance=user)
        details_form = UserDetailsForm(request.POST, instance=user_details)

        if user_form.is_valid() and details_form.is_valid():
            # Save both the user and user_details
            user_form.save()
            details_form.save()

            # Redirect to the user profile after updating
            return redirect('user-profile', pk=user.id)
        
    
        print(context)
    return render(request,"base/update-user.html",context)





def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) 
                                |Q(name__icontains=q) 
                                |Q(description__icontains=q)
                                )# to get filterd objects with topic name provided form Room 
    
    
    room_cont = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    topic = Topic.objects.all()[0:5]# to get all entity from topic

    context = {'rooms':rooms,'topics':topic,'room_count':room_cont,'room_messages':room_messages}
    return render(request,'base/home.html',context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')

        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {'room':room,'room_messages':room_messages,'participants':participants}        
    return render(request,'base/room.html',context)

@login_required(login_url='login')
def creatroom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created =Topic.objects.get_or_create(name=topic_name)
        #this statement is user for when user not select avilable topics so user can crate ther own topic
        Room.objects.create(

            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        
        return redirect('home')
        
    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateroom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all() 
    

    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        topic_name = request.POST.get("topic")
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    
    
    context={'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteroom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deletemessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("Your are not allowed here ")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,"base/topics.html",{'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request,"base/activity.html",{'room_messages': room_messages})

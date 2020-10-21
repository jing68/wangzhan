from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from socialnetwork.forms import  LoginForm, RegistrationForm,GlobalForm,ProfileForm
from socialnetwork.models import *

def login_action(request):
    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'login.html', context)
        print("hello1")
    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form
    print("hello2")
    # Validates the form.
    if not form.is_valid():
        return render(request, 'login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))
   
def logout_action(request):
    logout(request)
    print('i am out')
    return redirect(reverse('login'))

def register_action(request):
    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)
    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form
    # Validates the form.
    if not form.is_valid():
        return render(request, 'register.html', context)
    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])    
    login(request, new_user)
    profile = Profile(user=request.user)
    profile.save()
    return redirect(reverse('home'))

@login_required
def global_stream(request):
    context = {} 
    context = {'posts': Post.objects.all()}
    context['form'] = GlobalForm()
    if request.method =='GET':
        return render(request, 'global.html', context)
    new_post = Post(user = request.user,
                    datetime = timezone.now(),
                    username=request.user.username)                    
    form = GlobalForm(request.POST, instance=new_post)

    if not form.is_valid():
        context['form']=form
    else:
        form.save()
        context['form'] = GlobalForm()
    context['posts'] = Post.objects.all()
    return render(request,'global.html',context)

@login_required
def follower_stream(request):
    context={}
    context['posts']=Post.objects.all()
    
    current_user = Profile.objects.filter(user_id=request.user.id).latest('id')
    followlist = current_user.follower.all().values()
    followlist =[x['username'] for x in followlist]
    context['followlist'] = followlist
    
    return render(request,'follower.html',context)

@login_required
def profile_logged_in(request):
    
    item = Profile.objects.select_for_update().get(user=request.user)
    context={}
    current_user = Profile.objects.get(user=request.user)
    followlist = current_user.follower.all().values()
    follower_ids = [x["id"] for x in followlist]
    all_user = User.objects.all()
    context['users'] = all_user
    context['followlist'] = follower_ids
    
    if request.method=='GET':
        # if temp:
            # context = {'pic': temp, 'form': ProfileForm(initial={'bio_input_text': temp.bio_input_text}) }
        context['item'] = item
        context['form'] =ProfileForm(initial={'bio_input_text':item.bio_input_text})
        return render(request,'profile.html',context)

  
    form = ProfileForm(request.POST, request.FILES)
    if not form.is_valid():
        context={'item':item,'form':form}
        return render(request,'profile.html',context)

    pic = form.cleaned_data['Profile_Picture']
    print('Uploaded picture: {} (type={})'.format(pic,type(pic)))

    item.Profile_Picture=form.cleaned_data['Profile_Picture']
    item.content_type = form.cleaned_data['Profile_Picture'].content_type
    item.bio_input_text = form.cleaned_data['bio_input_text']
    item.save()
    context['item'] =item
    context['form'] = ProfileForm(initial={'bio_input_text':item.bio_input_text})  
    
    return render(request,'profile.html',context)


@login_required
def other_profile(request, user_id): #get user_id from global.html, this is user_id for who send post
    print('user id:',user_id)
    context={}
    user = get_object_or_404(User, id=user_id) #从User table取一条数据
    try:
        temp = Profile.objects.filter(user_id=user_id).latest('id')    #从Profile table取一条数据 
    except Profile.DoesNotExist:
        temp=None
    context['profile_user'] = user # profile_user.id: User table PK
    context['item']=temp # item.id: profile table PK
    
    current_user = Profile.objects.filter(user_id=request.user.id).latest('id')
    followlist= current_user.follower.all().values()
    followlist=[x['username'] for x in followlist] #show who i have followed 
    context={'profile_user':user,'item':temp,'followlist':followlist}

    if request.method=="POST":
        print("i am here")
        print(request.user.id)
        if 'follow' in request.POST:                     
            current_user.follower.add(user_id) #add a relationship
            followlist= current_user.follower.all().values()
            followlist=[x['username'] for x in followlist] #show who i have followed 
            context={'profile_user':user,'item':temp,'followlist':followlist}
            print(user_id)
            print('follow success')
        if 'unfollow' in request.POST:
            print('remove')
            current_user.follower.remove(user_id)
            followlist= current_user.follower.all().values()
            followlist=[x['username'] for x in followlist]
            context={'profile_user':user,'item':temp,'followlist':followlist}
    return render(request,'other_profile.html',context)


@login_required
def get_photo(request, id):
    item = get_object_or_404(Profile, id=id)
    
    if not item.Profile_Picture:
        raise Http404

    return HttpResponse(item.Profile_Picture, content_type=item.content_type)


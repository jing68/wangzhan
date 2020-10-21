from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from socialnetwork.forms import  LoginForm, RegistrationForm,GlobalForm,ProfileForm
from socialnetwork.models import *
import json

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
                    user_fullname = request.user.first_name +' '+request.user.last_name,
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


def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    print('_my_json_error_response')
    return HttpResponse(response_json, content_type='application/json', status=status)


def add_comment(request,id): # id 为post的id
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=404)

    if not 'item' in request.POST or not request.POST['item']:  # item为global.html中input comment中的name
        return _my_json_error_response("You must enter a comment to submit.")

    new_post = Post.objects.get(id=id)  # 第二个id为post.id
    new_item = Comment(comment_input_text=request.POST['item'], 
                       user = request.user,
                       comment_date_time = timezone.now(),
                       comment_profile = request.user.first_name +' '+request.user.last_name,
                       mypost = new_post)
    new_item.save()

    print('add_comment is called')
    return refresh_global(request)


def get_list(request):
    response_data = []
    for model_item in Comment.objects.all():
        my_item = {
            'id': model_item.id,
            'comment_input_text': model_item.comment_input_text,
            'user': model_item.user.username,
            'comment_profile':model_item.comment_profile,  
            'mypost_id':model_item.mypost_id,       
            # 'comment_date_time': model_item.comment_date_time
        }
        response_data.append(my_item)
    response_json = json.dumps(response_data)

    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    print('get_list')
    return response  #response是所有comment的数据

def refresh_global(request):
    response_posts = []
    response_comments = []
    login_user = User.objects.get(id=request.user.id)
    login_user_id = login_user.id

    for model_item in Post.objects.all():
        my_post = {
            'id':model_item.id,
            'user_id':model_item.user_id,
            'post_input_text':model_item.post_input_text,
            'user':model_item.username,
            'user_fullname':model_item.user_fullname,
            'datetime': model_item.datetime.astimezone().strftime("%m/%d/%Y %I:%M%p")
        }
        response_posts.append(my_post)
        print('the response post are',response_posts)

    for model_item in Comment.objects.all():
        my_comment = {
            'id': model_item.id,
            'user_id':model_item.user_id,
            'comment_input_text': model_item.comment_input_text,
            'user': model_item.user.username,
            'comment_profile':model_item.comment_profile,  
            'mypost_id':model_item.mypost_id,       
            'comment_date_time': model_item.comment_date_time.astimezone().strftime("%m/%d/%Y %I:%M%p")
        }
        response_comments.append(my_comment)
    
    response_data = {'response_posts':response_posts,'response_comments':response_comments,'login_user_id':login_user_id}
    response_json = json.dumps(response_data)

    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    print('refresh global completed')
    return response  #response是所有的数据

def refresh_follower(request):
    response_posts = []
    response_comments = []
    login_user = User.objects.get(id=request.user.id)
    login_user_id = login_user.id

    current_user = Profile.objects.get(user_id=request.user.id)
    followlist = current_user.follower.all().values()
    followlist =[x['username'] for x in followlist]

    for model_item in Post.objects.all():
        my_post = {
            'id':model_item.id,
            'user_id':model_item.user_id,
            'post_input_text':model_item.post_input_text,
            'user':model_item.username,
            'user_fullname':model_item.user_fullname,
            'datetime': model_item.datetime.astimezone().strftime("%m/%d/%Y %I:%M%p")
        }
        response_posts.append(my_post)
        print('the response post are',response_posts)

    for model_item in Comment.objects.all():
        my_comment = {
            'id': model_item.id,
            'user_id':model_item.user_id,
            'comment_input_text': model_item.comment_input_text,
            'user': model_item.user.username,
            'comment_profile':model_item.comment_profile,  
            'mypost_id':model_item.mypost_id,       
            'comment_date_time': model_item.comment_date_time.astimezone().strftime("%m/%d/%Y %I:%M%p")
        }
        response_comments.append(my_comment)
    
    response_data = {'response_posts':response_posts,'response_comments':response_comments,'login_user_id':login_user_id,'followlist':followlist}
    response_json = json.dumps(response_data)

    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    print('refresh global completed')
    return response  #response是所有的数据
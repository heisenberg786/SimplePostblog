from django.shortcuts import render
from basic_app.forms import UserProfileInfoForm, UserForm,PostForm
from basic_app.models import Post
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

# we want that the user which has logged in that users can only logged out we can use decorators
@login_required
def post(request):
    Post = PostForm()
    if request.method == 'POST':
        Post = PostForm(request.POST)
        if Post.is_valid():
            Post.save(commit=True)
            return HttpResponseRedirect(reverse('index'))

        else:
            return HttpResponse("Content in Post is Invalid")
    else:

        return render(request,'post.html',{'Post':Post})
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        # object banayga jo input dalenge vo user_form and profile_form mai aajayga
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # user mai password hash ke form mai store hoga
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            msg = user_form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + msg)

            # ye same process profile_form ke liye nai kr skhte qki overlap ho skhta h
            profile = profile_form.save(commit=False)
            profile.user = user
            # agr pic dala h vo request.FILES mai aajayga
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'basic_app/registeration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


def user_login(request):
    user_form = UserForm(data=request.POST)
    if request.method == 'POST':
        # ye form humne html mai banaya h isliye request.POST.get use kiya h
        username = request.POST.get('username')
        password = request.POST.get('password')
        # this one line will authenticate username and password
        user = authenticate(username=username, password=password)
        # if user is authenticate and active
        if user:
            if user.is_active:
            # if user is active then log tr = username

                login(request, user)

                return HttpResponseRedirect(reverse('post'))
            else:
                return HttpResponse("Account is not active")
        else:


            return HttpResponse("<h1>invalid login details supplied!</h1")
    else:
        return render(request,'basic_app/login.html',{})



# @login_required
def allpost(request):
    post = Post.objects.all()
    return render(request,'posting.html',{'post':post})

from myapp.jwt_auth import login, logout, is_authenticated, needs_authentication
from myapp.models import *
from myapp.forms import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


@needs_authentication
def signout(request):
	logout(request, '/')
	return redirect('/')

def signup(request):
    form = SignUpForm()
    submit_url = '/submit-signup/'
    return render(request, 'index_unsigned.html', {'form': form, 'submit_url': submit_url})

def handleLoginRequest(request):
    if request.method == "GET":
        return HttpResponse(status = 405)

    username = request.POST['username']
    password = request.POST['password']
    form = SignInForm()
    user = authenticate(username=username, password=password)
    if user:
        print("ascsdk")
        return login(request, user, '/')
    return render(request, 'index_unsigned.html', {'msg':'Invalid credentials entered',  'form':form})

def handleSignupRequest(request):
    if request.method == "GET":
        return HttpResponse(status = 405)
    formData = SignUpForm(request.POST)
    if formData.is_valid():
        user = formData.save(commit = False)
        user.password = make_password(user.password)
        user.save()
        return redirect('/')
    return render(request, 'index_unsigned.html', {'msg':'Invalid credentials entered', 'form':form})

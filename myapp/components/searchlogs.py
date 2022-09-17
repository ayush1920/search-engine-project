from .jwt_auth import login, logout, is_authenticated, needs_authentication
from myapp.models import *
from django.shortcuts import render, redirect

@needs_authentication
def logs(request):
	logs = Log.objects.all()
	return render(request, 'logs.html', {'logs':logs})

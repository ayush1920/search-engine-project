from .jwt_auth import login, logout, is_authenticated, needs_authentication
from myapp.models import *
from myapp.serializers import HistorySerializer
from rest_framework import viewsets
from django.shortcuts import render, redirect
from dateutil import parser
import psutil, os, logging, datetime

class HistoryView(viewsets.ModelViewSet):
	queryset = History.objects.all()
	serializer_class = HistorySerializer

@needs_authentication
def history(request):
	histories = History.objects.all().order_by("-id")
	return render(request, 'history.html', {'history':histories})

@needs_authentication
def transactions(request):
	if request.method=="POST":
		from_date = parser.parse(request.POST['from_date'])
		to_date = parser.parse(request.POST['to_date']) + datetime.timedelta(days=1)
		if from_date > to_date:
			return HttpResponse("To date cannot be less than from date")
		transactions = History.objects.filter(
			timestamp__gte=from_date, 
			timestamp__lte=to_date)
		return render(request, 'transactions.html', {'transactions':transactions})
	return render(request, 'transactions.html', {})
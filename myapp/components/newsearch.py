from .jwt_auth import login, logout, is_authenticated, needs_authentication
from myapp.models import *
from django.shortcuts import render, redirect
import psutil, os

def search_files(search_query, disk):
	search_result = []
	for dirs, subdirs, files in os.walk(disk):
		for file in files:
			if search_query.lower() in file.lower():
				search_result.append(os.path.join(dirs, search_query))	
	return search_result

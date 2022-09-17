import psutil
import os
import logging
import datetime
from django.shortcuts import render, redirect
from dateutil import parser
from .components.search_handler import SearchMulti
from .components.userauthentication import *
from .components.finddrives import *
from .components.searchhistory import *
from .components.newsearch import *
from .components.searchlogs import *
from .components.notifications import *
from .components.analytics import *
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import *
from .forms import *
from .serializers import HistorySerializer


def index(request):
    if is_authenticated(request):
        disks = my_disks()
        dutil = []
        pct_use = []
        for i in disks:
            dutil = psutil.disk_usage(i.device)
            pct_use.append([disks, dutil[3]])
        return render(request, 'index.html', {'disks': disks, 'use': pct_use})
    form = SignInForm()
    submit_url = '/login/'
    return render(request, 'index_unsigned.html', {'form': form, 'submit_url': submit_url})


def search_files(request, search_query, disk, thread_count):
    search_result = None
    search_time = None
    search_space = []
    if disk == "all":
        parts = psutil.disk_partitions()
        for part in parts:
            search_space.append(part.mountpoint)
    else:
        search_space.append(disk)
    search_result, search_time = SearchMulti(search_query, search_space, thread_count)

    return (search_result, search_time)


@needs_authentication
def search(request):
	search_query = request.GET.get('search').lower()
	force_search = bool(request.GET.get('force', False))
	dir_path = request.GET.get('dir_path', None)
	thread_count = int(request.GET.get('thread_count', 5))

	if not os.path.exists(dir_path):
		disks = my_disks()
		dutil = []
		pct_use = []
		for i in disks:
			dutil = psutil.disk_usage(i.device)
			pct_use.append([disks, dutil[3]])
		return render(request, 'index.html', {'disks': disks, 'use': pct_use, "msg": "Path doesn't exists."})

	force_search = bool(dir_path)
	result_from_db = History.objects.filter(search_query__icontains=search_query) if not force_search else None
	if result_from_db:
		return render(request,
						'search-results.html',
						{'search_query': search_query,
						'result_from_db': list(result_from_db.values()),
						"time_taken": "0.15",
						})
	else:
		try:
			file_extension = search_query.split(".")[1]
		except:
			file_extension = "invalid"
		selected_disk = request.GET.get('selected_disk', "all")
		paths = dir_path or selected_disk
		result, time_taken = search_files(request, search_query, paths, thread_count)
		if len(result) > 0:
			for filepath in result:
				filename = filepath.split("\\")[-1]
				History.objects.update_or_create(search_query=filename.lower(),
												selected_disk=selected_disk,
												result=filepath,
												file_extension=file_extension,
												user=request.user)
		else:
			new_log = Log.objects.create(search_query=search_query.lower(),
										selected_disk=selected_disk,
										result="Not found",
										file_extension=file_extension)
			new_log.save()
		return render(request, 'search-results.html',
					{'search_query': search_query, 'result': result, 'time_taken': time_taken})


def delete_history(request, id):
	selected_history = History.objects.get(id=id)
	selected_history.delete()
	notify(request)
	return redirect("/history/")

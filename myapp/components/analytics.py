from .jwt_auth import login, logout, is_authenticated, needs_authentication
from myapp.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect


@needs_authentication
def analytics(request):
	return render(request, 'analytics.html', {})

class ChartData(APIView):

    def get(self, request, format=None):
        list1 = []
        for ele in History.objects.values('file_extension'):
            list1.append(ele['file_extension'])
        print(list1)
        count=[]
        for i in set(list1):
            count.append(list1.count(i))

        labels = list(set(list1))
        chartLabel = "my data"
        print(labels,count)

        data = {
            "labels": labels,
            "chartLabel": chartLabel,
            "chartdata": count,
        }
        return Response(data)

from .jwt_auth import login, logout, is_authenticated, needs_authentication
from myapp.models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse  
from django.core.mail import send_mail
from django.conf import settings
   
def notify(request):  
    subject = "Greetings from SEH"  
    msg     = "One search record has been deleted"  
    to      = "pythonuser@gmail.com"  
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  
    if(res == 1):  
        msg = "Mail Sent Successfully."  
    else:  
        msg = "Mail Sending Failed."  
    return HttpResponse(msg)  

